from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time
import re

def scroll_page(driver, num_of_scroll=1, sleep_time=0.2):
    """
    Scrolls the page to load dynamic content.
    :param driver: Selenium WebDriver object
    :param num_of_scroll: Number of times to scroll the page
    :param sleep_time: Time in seconds to wait after each scroll (default is 0.5 seconds)
    """
    actions = ActionChains(driver)
    for _ in range(num_of_scroll):
        actions.send_keys(Keys.PAGE_DOWN).perform()

def initialize_webdriver():
    """Setup and return a Chrome browser with incognito mode and disabled images."""
    chrome_options = Options()
    chrome_options.add_argument("--incognito")

    # Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_search_terms():
    """
    Get search terms from the user and return as a list.
    """
    search_terms_input = input("Enter the search terms separated by commas: ")
    search_terms_input = search_terms_input.replace(',', ' ')  # Replace commas with spaces
    return search_terms_input.split()  # Split by spaces

def change_zip_code(driver, zip_code):
    """
    Change the ZIP code for Amazon delivery location.
    """
    # Click the delivery location link
    delivery_location = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "nav-global-location-popover-link"))
    )
    delivery_location.click()

    # Wait and enter the ZIP code
    zip_input = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "GLUXZipUpdateInput"))
    )
    zip_input.send_keys(zip_code)

    # Click the submit button to change the ZIP
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit'][@aria-labelledby='GLUXZipUpdate-announce']"))
    ).click()

    # Confirm the ZIP code change
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[2]/span/span/input'))
    ).click()


def wait_for_element(driver, by, value, timeout=2):
    """
    Wait for an element to be located in the DOM and return it.
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def get_last_page_number(driver, search_term):
    """
    Debug version: Get the last page number for the given search term.
    """
    try:
        last_page_element = wait_for_element(
            driver, By.XPATH, '//span[@class="s-pagination-item s-pagination-disabled" and @aria-disabled="true"]'
        )
        last_page_text = last_page_element.text
        last_page_match = re.search(r'\d+', last_page_text)

        if last_page_match:
            return int(last_page_match.group())
        else:
            print("Debug: Last page number not found.")
            return -1
    except Exception as e:
        print(f"Debug: Error in get_last_page_number: {e}")
        return -1


def get_asins_on_page(driver, scraped_asins):
    """
    Extract ASINs from the current page and return them as a list.
    """
    # Wait for the page to fully load
    scroll_page(driver)
    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@data-asin]'))
    )

    # Get the HTML content of the search results page
    html_content = driver.page_source

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find ASINs using the specified XPath
    asin_elements = soup.find_all("div", attrs={"data-asin": True})

    page_asins = []
    for element in asin_elements:
        asin = element["data-asin"]
        if asin and asin not in scraped_asins:  # Check if ASIN is not empty and not already scraped
            page_asins.append(asin)
            scraped_asins.add(asin)

    return page_asins

def navigate_to_next_page(driver):
    """
    Debug version: Navigate to the next search results page.
    Returns False if not possible.
    """
    try:
        next_buttons = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label*="Go to next page"]')
        if not next_buttons:
            print("Debug: Next button not found.")
            return False

        for button in next_buttons:
            if "s-pagination-button-disabled" not in button.get_attribute("class"):
                button.click()

                time.sleep(4)

                return True
        print("Debug: Next button disabled.")
        return False
    except Exception as e:
        print(f"Debug: Error in navigate_to_next_page: {e}")
        return False

def save_asins_to_csv(asins, filename):
    """
    Save ASINs to a CSV file.
    """
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ASINs'])
        for asin in asins:
            writer.writerow([asin])


def main():
    WAIT_TIME = 4  # Set this as a constant at the beginning of the function

    driver = None  # Initialize driver to None
    try:
        # Initialize WebDriver
        driver = initialize_webdriver()
        driver.get("https://www.amazon.com/ref=nav_logo")

        # Initialize other variables
        all_asins = set()
        scraped_asins = set()

        # Get User Input
        search_terms = get_search_terms()

        # Change ZIP code
        zip_code_to_use = '33180'
        print(f"\nChanging ZIP code to: {zip_code_to_use}\n")
        change_zip_code(driver, zip_code_to_use)
        time.sleep(2)

        # Loop through each search term to scrape ASINs
        for search_term in search_terms:
            search_bar = WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
            search_bar.clear()
            search_bar.send_keys(search_term)
            search_bar.send_keys(Keys.RETURN)

            last_page = get_last_page_number(driver, search_term)
            print(f"\nTotal Pages for '{search_term}': {last_page}\n")

            term_asins = set()
            page_number = 1

            while True:
                # Scroll the page to load all ASINs
                scroll_page(driver)

                # Extract ASINs and update the sets
                page_asins = get_asins_on_page(driver, scraped_asins)
                term_asins.update(page_asins)

                print(f"\nPAGE {page_number} --- ASINs extracted for '{search_term}': {len(page_asins)}\n")
                page_number += 1

                # Navigate to the next page and sleep only if needed
                if page_number > last_page or not navigate_to_next_page(driver):
                    break


            all_asins.update(term_asins)
            print(f"\nTOTAL ASINs FOR '{search_term}': {len(term_asins)}\n")

        # Export to CSV
        total_asins = len(all_asins)
        print(f"\nTOTAL ASINs FOUND FOR ALL KEYWORDS: {total_asins}\n")
        filename = f"{total_asins} ASINS.csv"
        save_asins_to_csv(all_asins, filename)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:  # Check if driver is initialized
            driver.quit()


main()