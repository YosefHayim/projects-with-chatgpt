from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from lxml import html
import re
from datetime import datetime
import os
import pickle
import csv
import traceback

# Function to save cookies to a file
def save_cookies(driver, location):
    pickle.dump(driver.get_cookies(), open(location, "wb"))

# Function to load cookies from a file and add them to the browser session
def load_cookies(driver, location):
    if os.path.exists(location):
        cookies = pickle.load(open(location, "rb"))
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver.add_cookie(cookie)

# Function to clean text by removing unwanted characters
def clean_text(text):
    clean = text.encode('ascii', 'ignore').decode('ascii')
    clean = re.sub(r'[^\w\s.,;!?\'"&$%-/()]', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def read_asins_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        asins = [row[0] for row in csv_reader]
    return asins

def is_blacklisted(asin, blacklist_path='blacklist.txt'):
    with open(blacklist_path, mode='r', encoding='utf-8') as file:
        blacklist = file.read().splitlines()
    return asin in blacklist or any(asin in s for s in blacklist)


def fetch_product_data(asin, driver):
    url = f"https://www.amazon.com/dp/{asin}"
    driver.get(url)

    page = html.fromstring(driver.page_source)

    product_data = {'ASIN': asin}

    try:

        # Category - Fetch the last category from the breadcrumbs
        category = page.xpath('//ul[contains(@class, "a-unordered-list a-horizontal a-size-small")]//li[last()]/span/a/text()')
        product_data['Category'] = clean_text(category[0]) if category else 'Category not found'

        # Brand Name
        brand = page.xpath('//a[@id="bylineInfo"]/text()')
        if brand:
            brand_text = clean_text(' '.join(brand))  # Join all text elements
            # Use regular expression to extract the brand name
            match = re.search(r'(Brand: )?(Visit the )?([\w\s]+?)( Store)?$', brand_text)
            if match:
                product_data['Brand'] = match.group(3).strip()  # Group 3 should be the brand name
            else:
                product_data['Brand'] = 'Brand not found'
        else:
            product_data['Brand'] = 'Brand not found'

        # Current Date
        product_data['Extraction Date'] = datetime.now().strftime("%Y-%m-%d")

        # Title
        title = page.xpath('//span[@id="productTitle"]/text()')
        product_data['Title'] = clean_text(title[0]) if title else 'Title not found'

        # Price
        price = page.xpath('//span[contains(@class, "a-price")]/span[@class="a-offscreen"]/text()')
        product_data['Price'] = clean_text(price[0]) if price else 'Price not found'

        # Percent Savings
        percent_savings = page.xpath('//span[contains(@class, "savingsPercentage")]/text()')
        product_data['Percent Savings'] = clean_text(percent_savings[0]) if percent_savings else 'Percent savings not found'

        # Coupon Data
        coupon_data = page.xpath('//label[starts-with(@id, "couponText")]/text()')
        # Extracting the coupon amount or percentage
        coupon_amount = page.xpath('//label[starts-with(@id, "couponText")]/text()')
        if coupon_amount:
            # The text might include extra whitespace and other characters, so we clean it
            coupon_text = clean_text(' '.join(coupon_amount))
            product_data['Coupon'] = coupon_text
        else:
            product_data['Coupon'] = 'Coupon not found'

        # Delivery Time
        delivery_time_secondary = page.xpath(
            '//div[@id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE"]//span[@class="a-text-bold"]/text()')
        product_data['Delivery Time'] = clean_text(
            delivery_time_secondary[0]) if delivery_time_secondary else 'Delivery time not found'

        # Secondary Delivery Message
        secondary_delivery_message = page.xpath('//div[@id="mir-layout-DELIVERY_BLOCK-slot-SECONDARY_DELIVERY_MESSAGE_LARGE"]//text()')
        # Join the extracted parts to form the full message and clean it
        product_data['Secondary Delivery Message'] = clean_text(' '.join(secondary_delivery_message).strip()) if secondary_delivery_message else 'Secondary delivery message not found'

        # Stock Status
        stock_status = page.xpath('//div[@id="availability"]//text()')
        stock_status = list(filter(None, (clean_text(status) for status in stock_status)))
        product_data['Stock Status'] = stock_status[0] if stock_status else 'Stock status not found'

        # Quantity Options - Get only the last quantity count
        quantity_options = page.xpath('//select[contains(@id, "quantity")]/option[last()]/text()')
        product_data['Last Quantity Count'] = clean_text(
            quantity_options[0]) if quantity_options else 'Last quantity count not found'

        # Gift Option Available
        gift_option = page.xpath('//input[@id="gift-wrap"]/@value')
        product_data['Gift Option Available'] = True if gift_option else False

        # Product Description
        description = page.xpath('//div[@id="feature-bullets"]//span[@class="a-list-item"]/text()')
        product_data['Description'] = ' | '.join(
            clean_text(desc) for desc in description) if description else 'Description not found'

        # Product Details
        product_details = {}
        product_details_table = page.xpath('//div[@class="a-section a-spacing-small a-spacing-top-small"]//tr')
        for detail in product_details_table:
            key = detail.xpath('.//td[@class="a-span3"]//span/text()')
            value = detail.xpath('.//td[@class="a-span9"]//span/text()')
            if key and value:
                # Since the brand is extracted separately, we skip it here
                if 'Brand' not in key[0]:
                    product_details[clean_text(key[0])] = clean_text(value[0])

        product_data['Product Details'] = product_details if product_details else 'Product details not found'

        # Warning
        warning = page.xpath('//div[contains(@class, "a-alert-warning")]//div[@class="a-alert-content"]/text()')
        product_data['Warning'] = clean_text(warning[0]) if warning else 'Warning not found'

        # Returns Policy
        returns_policy = page.xpath('//div[contains(@offer-display-feature-name, "desktop-return-info")]//span[contains(@class, "offer-display-feature-text-message")]/text()')
        product_data['Returns Policy'] = clean_text(returns_policy[0]) if returns_policy else 'Returns policy not found'

        # Image URLs
        image_elements = page.xpath('//div[contains(@id, "imageGallery") or contains(@id, "altImages")]//img/@src')
        high_res_image_urls = []

        # Define a regular expression pattern to find and replace the resolution part of the image URL
        # This pattern will match the part of the URL right after 'images/I/' until the next underscore.
        resolution_pattern = re.compile(r'(images/I/[^/]+)\._[^_.]+_')

        # Define a pattern for images that should be excluded
        exclusion_pattern = re.compile(r'_PKdp-play-icon-overlay__')

        for image in image_elements:
            if 'https://m.media-amazon.com/images/I/' in image and not exclusion_pattern.search(image):
                # Replace the resolution part with '_AC_SY1000_' to request the high-resolution image
                high_res_image = resolution_pattern.sub(r'\1._AC_SY1000_', image)
                high_res_image_urls.append(high_res_image)

        # Remove duplicates and sort to maintain order
        high_res_image_urls = sorted(set(high_res_image_urls), key=high_res_image_urls.index)

        # Assign each high-resolution image URL to its own key in the product_data dictionary
        for index, high_res_image in enumerate(high_res_image_urls, start=1):
            product_data[f'Image URL {index}'] = high_res_image

        # If there are no high-resolution images found, add a placeholder for the first image column
        if not high_res_image_urls:
            product_data['Image URL 1'] = 'High-resolution image URLs not found'




    except Exception as e:
        # Handle any exception that occurs during the data fetching
        print(f"Error fetching data for ASIN {asin}: {e}")
        return None  # Return None if there was an error

    return product_data


def main():
    # Setup Selenium WebDriver
    options = Options()
    service = Service('/eBay Dropshipping/eBay None API Lister/Getting Products Details/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    # Load cookies if available
    cookies_location = 'cookies.pkl'  # Update the path if necessary
    load_cookies(driver, cookies_location)

    # Read ASINs from the CSV file
    asins = read_asins_from_csv('ASINS_EXTRACTION.csv')

    # Initialize variables
    output_file = 'DATA_EXPORTED.csv'
    fieldnames = None  # To be populated later
    existing_data = []  # To store existing data in case of updating fieldnames

    input("Perform any manual actions in the browser now and press Enter when ready to continue with data fetching...")

    try:
        for asin in asins:
            if is_blacklisted(asin):
                print(f"The ASIN {asin} is blacklisted and will be skipped.")
                continue

            product_data = fetch_product_data(asin, driver)
            if product_data:
                if fieldnames is None:
                    # Initialize fieldnames and write the first product
                    fieldnames = sorted(product_data.keys(), key=lambda k: (k.startswith('Image URL'), k))
                    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow(product_data)
                else:
                    new_fields = set(product_data.keys()) - set(fieldnames)
                    if new_fields:
                        # Update fieldnames
                        fieldnames.extend(sorted(new_fields, key=lambda k: (k.startswith('Image URL'), k)))

                        # Read existing data
                        with open(output_file, mode='r', newline='', encoding='utf-8') as csvfile:
                            reader = csv.DictReader(csvfile)
                            existing_data = [row for row in reader]

                        # Rewrite file with updated fieldnames
                        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            for row in existing_data:
                                writer.writerow(row)

                    # Append new product data
                    with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow(product_data)

                print(f"Data for ASIN {asin} written to CSV.")

        print("Successfully finished processing all products.")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()