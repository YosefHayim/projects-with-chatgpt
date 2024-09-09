from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import csv
import time

def get_total_pages(driver):
    """
    Get the total number of pages.
    """
    try:
        total_pages_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[starts-with(@aria-label, "Page ") and contains(@class, "a-disabled")]'))
        )
        return int(total_pages_element.text)
    except Exception as e:
        print(f"Failed to retrieve the total number of pages: {str(e)}")
        return None

def export_to_csv(asins):
    """
    Export ASINs to a CSV file.
    """
    filename = f"{len(asins)}_asins.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ASIN'])
        for asin in asins:
            writer.writerow([asin])
    print(f"ASINs exported to {filename}")


def initialize_webdriver(url):
    """
    Initialize Selenium Webdriver and navigate to the URL.
    """
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def apply_filters(driver):
    """
    Apply various filters on the website.
    Clicks: All Categories, All Deals, All Discounts, All Prices, 4+ Stars, and specific categories.
    """
    # Define a function for waiting and clicking an element by its attributes and value
    def wait_and_click(attr, value):
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((attr, value))
        )
        element.click()

    try:
        # Click all categories
        wait_and_click(By.CSS_SELECTOR, 'a[data-testid="select-all-filter-desktop"]')

        # Click all deals
        wait_and_click(By.CSS_SELECTOR, 'a[data-csa-c-element-id="filter-deal-type-all"]')

        # Click all discounts
        wait_and_click(By.CSS_SELECTOR, 'a[data-csa-c-element-id="filter-discount-all"]')

        # Click all prices
        wait_and_click(By.CSS_SELECTOR, 'a[data-csa-c-element-id="filter-price-all"]')

        # Click 4+ stars
        wait_and_click(By.XPATH, '//span[@aria-label="Average review star rating of 4 and up"]')

        # Click baby category
        wait_and_click(By.CSS_SELECTOR, 'input[data-csa-c-element-id="filter-department-165796011"]')

        # Click baby cloth category
        wait_and_click(By.CSS_SELECTOR, 'input[data-csa-c-element-id="filter-department-7147444011"]')

        # Click books category
        wait_and_click(By.CSS_SELECTOR, 'input[data-csa-c-element-id="filter-department-283155"]')
        print('FILTERS HAS BEEN APPLIED...')
    except Exception as e:
        print(f"An error occurred: {e}")

def navigate_to_next_page(driver):
    """
    Navigate to the next page by clicking the "Next" button.
    """
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="Next"]'))
        )
        next_button.click()
        time.sleep(5)
        return True
    except Exception as e:
        print(f"Reached the end or failed to navigate to the next page: {str(e)}")
        return False


def extract_asins(html_content):
    """
    Extract ASINs from HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    product_cards = soup.select('.a-link-normal.DealCard-module__linkOutlineOffset_2fc037WfeGSjbFp1CAhOUn')

    asins = []
    for product_card in product_cards:
        href_content = product_card['href']
        for part in href_content.split('%7C'):
            if part.startswith('B'):
                asins.append(part)

    return asins


if __name__ == "__main__":
    url = "https://www.amazon.com/outlet/deals/ref=cg_outnav22_1d1_w?ref=outnav_4&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=top_2&pf_rd_r=HVXKMBBFEKZZP7TJZGRF&pf_rd_t=0&pf_rd_p=ee06844e-30d2-4c2d-803c-419b58cc10d7&pf_rd_i=outlet_desktop_home"  # Replace with your actual URL

    # Initialize WebDriver and navigate to the URL
    driver = initialize_webdriver(url)


    # Get total number of pages
    total_pages = get_total_pages(driver)
    if total_pages is None:
        print("Failed to retrieve the total number of pages.")
        driver.quit()
        exit(1)

    # Apply filters
    apply_filters(driver)
    time.sleep(4)
    all_asins = []
    try:
        for current_page in range(1, total_pages + 1):
            html_content = driver.page_source
            asins = extract_asins(html_content)
            all_asins.extend(asins)
            print(f"PAGE {current_page}/{total_pages}: {len(asins)} ASINs EXTRACTED.\n")

            if current_page < total_pages:
                navigate_to_next_page(driver)

    except KeyboardInterrupt:
        print("Script interrupted by user. Saving extracted ASINs...")
    except Exception as e:
        print(f"An error occurred: {str(e)}. Saving extracted ASINs...")

    export_to_csv(all_asins)
    driver.quit()