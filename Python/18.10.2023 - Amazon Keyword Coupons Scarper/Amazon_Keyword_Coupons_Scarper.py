from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.chrome.options import Options

import re
import time


# Constants
SEARCH_BAR_ID = "twotabsearchtextbox"
LAST_PAGE_XPATH = '//span[@class="s-pagination-item s-pagination-disabled" and @aria-disabled="true"]'
COUPON_CLASS = "a-size-base s-highlighted-text-padding aok-inline-block s-coupon-highlight-color"
DISCOUNT_CLASS = "a-size-base a-color-secondary a-text-strike"
NEXT_BUTTON_CSS = 'a[aria-label*="Go to next page"]'


def initialize_driver() -> webdriver.Chrome:
    # Create Chrome options object
    chrome_options = Options()

    # Disable images
    prefs = {
        "profile.managed_default_content_settings.images": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Create the WebDriver with the Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.amazon.com/")

    return driver


def get_search_terms() -> list:
    search_terms_input = input("\nHello, welcome to our Amazon COUPON&DISCOUNTS Scarper, please type here your keywords:\n")
    return search_terms_input.split(',')

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

def get_coupon_criteria() -> str:
    while True:
        print('REMINDER YOU CAN LEAVE IT EMPTY AND IT WILL FIND COUPONS FROM ALL RANGES')
        criteria = input("\nWhat is the number for COUPON ASINs?, please reply with an number between 5 to 100 with a jumps of 5:\n")
        if all(0 <= float(re.search(r"[-+]?\d*\.\d+|\d+", crit).group()) <= 100 for crit in re.findall(r"[-+]?\d*\.\d+|\d+", criteria)):
            return criteria
        print(f"The number {criteria} is not optionable, please try again.")


def get_discount_criteria() -> str:
    while True:
        criteria = input("\nWhat is the number for DISCOUNT ASINs?, please reply with an number between 5 to 100 with a jumps of 5:\n")
        if all(0 <= float(re.search(r"[-+]?\d*\.\d+|\d+", crit).group()) <= 100 for crit in re.findall(r"[-+]?\d*\.\d+|\d+", criteria)):
            return criteria
        print(f"The number {criteria} is not optionable, please try again.")


def find_last_page_number(driver: webdriver.Chrome, search_term: str) -> int:
    last_page_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, LAST_PAGE_XPATH))
    )
    last_page_text = last_page_element.text
    last_page_match = re.search(r'\d+', last_page_text)
    return int(last_page_match.group()) if last_page_match else -1


def find_asins_with_deals(driver, page_number, last_page, coupon_criteria, discount_criteria):
    asins_with_deals = {}
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Regex for extracting numerical values
    num_regex = r"[-+]?\d*\.\d+|\d+"

    # Correctly form the evaluation condition
    if coupon_criteria.isdigit():
        coupon_criteria = f"== {coupon_criteria}"
    if discount_criteria.isdigit():
        discount_criteria = f"== {discount_criteria}"

    # Filtering Coupons
    for element in soup.find_all("span", class_=COUPON_CLASS):
        deal_text = element.text
        extracted_number = float(re.search(num_regex, deal_text).group())
        evaluation_condition = f"{extracted_number} {coupon_criteria}"

        if 0 <= extracted_number <= 100 and eval(evaluation_condition):
            asin = element.find_previous("div", attrs={"data-asin": True})["data-asin"]
            asins_with_deals[asin] = deal_text

    # Filtering Discounts
    for element in soup.find_all("span", class_=DISCOUNT_CLASS):
        deal_text = element.text
        extracted_number = float(re.search(num_regex, deal_text).group())
        evaluation_condition = f"{extracted_number} {discount_criteria}"

        # Debug statement
        print(f"Debug - Discount: {deal_text}, Extracted: {extracted_number}, Eval condition: {evaluation_condition}")

        if 0 <= extracted_number <= 100 and eval(evaluation_condition):
            asin = element.find_previous("div", attrs={"data-asin": True})["data-asin"]
            asins_with_deals[asin] = deal_text

    print(f"PAGE {page_number}/{last_page} --- {len(asins_with_deals)} ASINs\n")
    return asins_with_deals


def main():
    try:
        driver = initialize_driver()
        search_terms = get_search_terms()
        coupon_criteria = get_coupon_criteria()
        discount_criteria = get_discount_criteria()
        asins_with_deals = {}
        total_pages_scraped = 0
        total_search_terms = []
        zip_code_to_use = '33180'
        print(f"\nChanging ZIP code to: {zip_code_to_use}\n")
        change_zip_code(driver, zip_code_to_use)
        time.sleep(2)

        should_proceed = True

        for search_term in search_terms:
            total_search_terms.append(search_term)
            search_bar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, SEARCH_BAR_ID))
            )
            search_bar.clear()
            search_bar.send_keys(search_term)
            search_bar.send_keys(Keys.RETURN)

            if should_proceed:
                proceed = input("Need to dive deeply to the filters? go ahead, once you finish press any key to continue.\n")
                should_proceed = False

            last_page = find_last_page_number(driver, search_term)
            print(f"TOTAL PAGES FOR '{search_term}': {last_page}\n")
            total_pages_scraped += last_page

            page_number = 1
            while True:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]'))
                )

                asins_with_deals.update(find_asins_with_deals(driver, page_number, last_page, coupon_criteria, discount_criteria))

                next_buttons = driver.find_elements(By.CSS_SELECTOR, NEXT_BUTTON_CSS)
                next_button = next((button for button in next_buttons if "s-pagination-button-disabled" not in button.get_attribute("class")), None)

                if next_button is None:
                    break

                next_button.click()
                time.sleep(3)
                page_number += 1

            print(f"TOTAL PAGES SCRAPED FOR '{search_term}': {last_page}\n")
            print(f"TOTAL ASINS FOUND FOR '{search_term}': {len(asins_with_deals)}\n")

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        total_asins = len(asins_with_deals)
        filename = f"{total_asins} ASINs.csv"

        with open(filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['ASINs', 'Coupon/Discount'])
            for asin, deal in asins_with_deals.items():
                writer.writerow([asin, deal])

        print(f"TOTAL ASINs: {total_asins}")
        print(f"TOTAL PAGES SCRAPED: {total_pages_scraped}")
        print(f"TOTAL KEYWORDS SCRAPED: {', '.join(total_search_terms)}")


if __name__ == "__main__":
    main()