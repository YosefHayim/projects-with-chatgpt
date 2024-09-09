from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re
import time
import csv
import urllib.parse

def configure_chrome_options():
    chrome_options = Options()

    # Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # Disable JavaScript
    chrome_options.add_argument("--disable-javascript")

    # Set default language to US English
    chrome_options.add_argument("--lang=en-US")

    return chrome_options


def sanitize_file_path(file_path):
    """Remove quotes from the file path if present."""
    return file_path.strip("\"")


def click_last_subcategory(driver, amazon_url):
    """Clicks the last subcategory on an Amazon page and extracts ASINs."""
    driver.get(amazon_url)
    asins = set()

    try:
        # Wait for the subcategories to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.a-unordered-list.a-horizontal.a-size-small"))
        )

        # Adding a delay of 2 seconds to make sure all elements are loaded
        time.sleep(3)

        # Locate the ul element and li elements
        ul_element = driver.find_element(By.CSS_SELECTOR, "ul.a-unordered-list.a-horizontal.a-size-small")
        li_elements = ul_element.find_elements(By.CSS_SELECTOR, "li span.a-list-item a.a-link-normal.a-color-tertiary")

        # Click the last subcategory
        li_elements[-1].click()

        # Wait for the product list to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a'))
        )

        # Extract ASINs from product URLs
        asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
        product_links = driver.find_elements(By.CSS_SELECTOR, 'a')
        for link in product_links:
            href = link.get_attribute('href')
            if href:
                asin_match = asin_pattern.search(href)
                if asin_match:
                    asins.add(asin_match.group(1))

        return list(asins)
    except Exception as e:
        print(f"An error occurred in click_last_subcategory: {e}")
        return []


def generate_google_search_url(query):
    """Generate a Google Search URL based on the query."""
    base_url = "https://www.google.com/search?q="
    query = urllib.parse.quote_plus(query)
    return f"{base_url}{query}"


def main():
    chrome_options = configure_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)

    # Initialize counters and container for ASINs
    total_titles = 0
    total_asins = 0
    all_asins = []

    # Get the CSV file path from the user
    raw_csv_file_path = input("Please enter the path to the CSV file: ")
    csv_file_path = sanitize_file_path(raw_csv_file_path)

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                query = row[0].strip()

                # Skip rows that are not product titles
                if query.lower() in ["title", "shop on ebay"]:
                    continue

                total_titles += 1

                url = generate_google_search_url(query)
                driver.get(url)
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a')))

                amazon_links = [a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, 'a') if
                                a.get_attribute('href') and "amazon" in a.get_attribute('href')]

                if amazon_links:
                    amazon_url = amazon_links[0]
                    asins = click_last_subcategory(driver, amazon_url)
                    total_asins += len(asins)
                    all_asins.extend(asins)
                    print(f"TITLE {total_titles} --- {len(asins)} ASINs")
                else:
                    print(f"TITLE {total_titles} --- 0 ASINs")

    except FileNotFoundError:
        print(f"File {csv_file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Save the ASINs to a CSV file
        with open(f"{total_asins} ASINs.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for asin in all_asins:
                csvwriter.writerow([asin])

        print(f"TOTAL TITLES SCRAPED: {total_titles}")
        print(f"TOTAL ASINs SCRAPED: {total_asins}")


if __name__ == "__main__":
    main()