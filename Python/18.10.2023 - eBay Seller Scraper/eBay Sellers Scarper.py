import csv
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from fuzzywuzzy import fuzz

def setup_browser():
    """Setup and return a Chrome browser with incognito mode and disabled images."""
    chrome_options = Options()
    chrome_options.add_argument("--incognito")

    # Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def read_csv(file_path):
    """Read product titles from CSV file and validate."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist at path: {file_path}")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def write_csv(file_path, data):
    """Write seller names to CSV file."""
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Product Title", "Seller Names"])
        for title, sellers in data:
            writer.writerow([title, ", ".join(sellers)])

def navigate_to_url_and_search(driver, product_title):
    """Navigate to eBay and perform the search."""
    url = "https://www.ebay.com/"
    driver.get(url)
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "gh-ac"))
    )
    search_box.send_keys(product_title)
    search_button = driver.find_element(By.ID, "gh-btn")
    search_button.click()

def extract_seller_names(driver, product_title, min_similarity=70):
    """Extract seller names based on product title similarity in search results."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.s-item__info'))
    )
    seller_names = []

    # Get all the titles and seller names from eBay search results
    title_elements = driver.find_elements(By.CSS_SELECTOR, '.s-item__title')
    seller_elements = driver.find_elements(By.CSS_SELECTOR, '.s-item__seller-info-text')

    for title_element, seller_element in zip(title_elements, seller_elements):
        title = title_element.text.lower()
        similarity = fuzz.token_sort_ratio(product_title.lower(), title)
        if similarity >= min_similarity:
            seller_name = re.search(r"([\w]+)", seller_element.text).group(1)
            seller_names.append(seller_name)

    return seller_names

def main():
    csv_file_location = input("Please enter the full path to your product titles CSV file: ").strip("\"")
    try:
        # Validate the file exists and read the product titles
        product_titles = read_csv(csv_file_location)
    except FileNotFoundError as e:
        print(e)
        return

    driver = setup_browser()
    data_to_export = []

    for idx, product_title in enumerate(product_titles):
        try:
            print(f"\nProcessing title {idx + 1} of {len(product_titles)}: {product_title}")
            navigate_to_url_and_search(driver, product_title)
            seller_names = extract_seller_names(driver, product_title, min_similarity=70)
            print(f"Total sellers found for this title: {len(seller_names)}")
            data_to_export.append((product_title, seller_names))
        except (NoSuchElementException, TimeoutException):
            print("No sellers found for this search.")
            continue
        except Exception as ex:
            print(f"An error occurred: {ex}")

    driver.quit()

    # Calculate and print the requested information
    total_sellers_found = sum(len(sellers) for _, sellers in data_to_export)
    total_titles_searched = len(product_titles)
    matching_ratio = (total_sellers_found / total_titles_searched) * 100
    script_run_time = time.perf_counter() - start_time

    print(f"\nTOTAL SELLERS FOUND: {total_sellers_found}...")
    print(f"MATCHING RATIO IS: {matching_ratio:.2f}%")
    print(f"TOTAL TIME THE SCRIPT RUN: {script_run_time:.2f} seconds...")

    # Generate the CSV file name based on the number of sellers found
    csv_name = f"Sellers Scarped_{total_sellers_found}.csv"
    export_path = os.path.join(r'/eBay Dropshipping/eBay Seller Scraper', csv_name)
    write_csv(export_path, data_to_export)
    print(f"\nExported data to {export_path}\n")

if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
