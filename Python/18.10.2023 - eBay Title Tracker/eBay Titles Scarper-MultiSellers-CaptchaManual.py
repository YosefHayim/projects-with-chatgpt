from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from lxml import html
import time
import random
import csv
from datetime import datetime

def setup_browser():
    """Setup and return a Chrome browser with incognito mode and disabled images."""
    chrome_options = Options()
    chrome_options.add_argument("--incognito")

    # Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def wait_for_element(driver, xpath, timeout=10):
    """Wait for an element to appear on the page."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def click_element(driver, xpath):
    """Click an element, waiting 1-2 seconds before the click and checking for CAPTCHA."""
    try:
        elem = wait_for_element(driver, xpath)
        sleep_time = random.uniform(1, 2)  # Random sleep time between 1 and 2 seconds
        time.sleep(sleep_time)

        # Check for CAPTCHA form in the HTML content
        page_content = driver.page_source
        tree = html.fromstring(page_content)
        captcha_form = tree.xpath('//form[@id="captcha_form"]')
        if captcha_form:
            handle_captcha_manually()

        elem.click()
    except TimeoutException as e:
        print(f"Timeout while waiting for element: {e}")
        driver.quit()
    except Exception as e:
        print(f"Unexpected error: {e}")
        driver.quit()


def navigate_to_url(driver, seller_name):
    """Navigate to the eBay URL for the given seller."""
    url = f"https://www.ebay.com/sch/i.html?_ssn={seller_name}&store_name={seller_name}&_oac=1&LH_Sold=1&LH_Complete=1"
    driver.get(url)


def interact_with_page(driver):
    """Perform various interactions on the eBay page."""
    try:
        click_element(driver, '//button[@title="Ship to"]')
        time.sleep(1)
        click_element(driver, '//button[@aria-label="Ship to:"]')
        click_element(driver, '//span[@class="flgspr flaus"]')
        time.sleep(1)
        click_element(driver, '//button[.//span[text()="Done"]]')

        print("-----------------------------------------SET FLAG USA DONE------------------------------------------------------\n")
        time.sleep(3)
        print('\nWaiting 3 Seconds to launch customization\n')
        click_burger = driver.find_element(By.CSS_SELECTOR,
                                           'button[aria-label="Listing options selector. List View selected."]')
        click_burger.click()
        time.sleep(2)

        click_customize = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Customize"]')
        click_customize.click()
        time.sleep(2)

        change_results_show = driver.find_element(By.CSS_SELECTOR, "input#cust-viewType-2")
        time.sleep(2)
        change_results_show.click()

        change_view_items = driver.find_element(By.ID, "cust-ipp-4")
        change_view_items.click()

        same_tab_icon = driver.find_element(By.ID, "cust-openVi-1")
        same_tab_icon.click()

        apply_changes = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply changes')]")
        apply_changes.click()
        print(
            "-----------------------------------------CUSTOMIZE PAGE DONE------------------------------------------------------\n")

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        driver.quit()


total_titles = []

def scrape_and_save_data(driver, seller_name):
    """Scrape data and add it to the global total_titles list."""
    global total_titles
    page_number = 0  # Initialize page number
    try:
        while True:
            page_number += 1  # Increment the page number for each loop iteration

            html_content = driver.page_source
            doc = html.fromstring(html_content)

            titles = doc.xpath('//span[@role="heading"]')
            titles_on_page = len(titles)  # Number of titles on the current page

            for title in titles:
                title_text = title.text_content()
                total_titles.append(title_text)

            print(f"\nPAGE {page_number} --- TITLES EXTRACTED {titles_on_page}/{titles_on_page} \n")

            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Go to next search page']"))
                )
                next_button.click()

            except NoSuchElementException:
                print("Next button not found. Exiting.")
                break

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def write_to_csv():
    """Write the global total_titles list to a single CSV file."""
    #timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    csv_filename = f"SELLERS TITLES {len(total_titles)}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Title"])
        for title in total_titles:
            csv_writer.writerow([title])

    print(f"\nTOTAL TITLES EXTRACTED {len(total_titles)}\n")
    print(f"\nSAVED ALL TITLES TO: {csv_filename}\n")


def handle_captcha_manually():
    """
    Pause the program to allow manual captcha solving.
    Continue when the user signals that the captcha is solved.
    """
    print("Captcha detected. Please solve the captcha manually.")
    input("Press Enter to continue after solving the captcha...")


MAX_RETRIES = 3  # Maximum number of retries for each seller
interaction_done = False  # Moved outside the function to retain its state across sellers


def process_seller(driver, seller_name, interaction_done):
    """Navigate to each seller's page and scrape data."""
    captcha_solved = False  # Initialize a flag for CAPTCHA

    for _ in range(MAX_RETRIES):
        try:
            # Navigate to the seller's URL
            navigate_to_url(driver, seller_name)
            time.sleep(1)  # Wait for 1 seconds

            # Check for CAPTCHA
            page_content = driver.page_source
            if "Please verify yourself" in page_content:
                handle_captcha_manually()
                captcha_solved = True  # Update the CAPTCHA flag

            # If CAPTCHA is solved, continue from the same URL
            if captcha_solved:
                navigate_to_url(driver, seller_name)
                time.sleep(1)  # Wait for 1 seconds
                captcha_solved = False  # Reset the CAPTCHA flag

            # Perform initial interaction if not done before
            if not interaction_done:
                interact_with_page(driver)
                interaction_done = True  # Update the flag after interaction

            scrape_and_save_data(driver, seller_name)
            print(f"SUCCESSFULLY FINISHED SCRAPING TITLES FROM THE SELLER: {seller_name}")
            break  # Success, exit the retry loop

        except Exception as e:  # Catch all exceptions for demonstration
            print(f"An error occurred: {e}")
            continue  # Go to the next iteration of the loop

    return interaction_done  # Return the current state of interaction_done


if __name__ == "__main__":
    try:
        seller_names_input = input("\nENTER THE NAME OF THE SELELRS BY COMMA SEPERATOR (SELLER1, SELLER2) : ")
        seller_names = [name.strip() for name in seller_names_input.split(',')]

        driver = setup_browser()
        interaction_done = False

        for seller_name in seller_names:
            print(f"\nMOVING TO THE NEXT SELLER: {seller_name}\n")
            interaction_done = process_seller(driver, seller_name, interaction_done)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        write_to_csv()
