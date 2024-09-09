# Amazon Coupon & Discount Scraper

This script automates the process of finding and extracting ASINs (Amazon Standard Identification Numbers) for products with specific coupon and discount criteria. It's useful for finding deals on Amazon or analyzing discounts for business purposes.

## Features

- **Coupon & Discount Filtering**: Automatically filters and extracts ASINs based on user-defined coupon and discount criteria.
- **ZIP Code Customization**: Changes the Amazon delivery location to a specified ZIP code for localized search results.
- **Dynamic Content Handling**: Scrolls through multiple pages of Amazon search results to capture all relevant ASINs.
- **CSV Export**: Saves the extracted ASINs and associated deals into a CSV file.

## Setup

### Prerequisites

- Python 3.x
- Selenium (`pip install selenium`)
- BeautifulSoup (`pip install beautifulsoup4`)
- ChromeDriver (ensure it matches your Chrome browser version)

### Installation

1. **Install the required Python packages**:
   ```bash
   pip install selenium beautifulsoup4
   ```

2. **Download ChromeDriver**:
   Download the correct version of ChromeDriver that matches your Chrome browser from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

3. **Place ChromeDriver in your PATH**:
   Ensure `chromedriver` is in your system's PATH or specify the path directly in the script.

## Usage

1. **Run the Script**:
   Start the script by running:
   ```bash
   python amazon_coupon_discount_scraper.py
   ```

2. **Input Search Terms**:
   When prompted, enter the search terms separated by commas (e.g., `laptop, phone case, bluetooth speaker`). The script will process each term individually.

3. **Specify Coupon & Discount Criteria**:
   - Input a number between `5` and `100` for coupon criteria (with jumps of 5), or leave it empty to find coupons across all ranges.
   - Specify discount percentage criteria similarly.

4. **ZIP Code Customization**:
   The script automatically changes the delivery location to the ZIP code `33180`. Modify this in the script if you need a different location.

5. **ASIN Extraction**:
   The script will navigate through Amazon search results, apply the specified filters, and extract ASINs that meet your criteria. Results will be saved to a CSV file named after the total number of ASINs found (e.g., `1234 ASINs.csv`).

## Script Overview

- **initialize_driver**: Sets up a Chrome browser with images disabled for faster loading.
- **change_zip_code**: Changes the Amazon delivery location to the specified ZIP code.
- **get_search_terms**: Prompts the user to input search terms, which are processed into a list.
- **get_coupon_criteria & get_discount_criteria**: Prompts the user to input coupon and discount criteria for filtering ASINs.
- **find_last_page_number**: Determines the last page of search results for each term.
- **find_asins_with_deals**: Filters ASINs based on coupon and discount criteria using BeautifulSoup.
- **CSV Export**: Saves the extracted ASINs and associated deals to a CSV file.

## Error Handling

The script includes error handling to manage issues like timeouts or missing elements. If an error occurs, it will log the error and continue processing the next search term.

## Customization

- **ZIP Code**: Adjust the ZIP code in the `change_zip_code` function to customize the delivery location.
- **Criteria Settings**: Modify the coupon and discount criteria functions to fine-tune the search filters.

## Notes

- Ensure your ChromeDriver version matches your installed version of Chrome to avoid compatibility issues.
- The script is designed to handle dynamic content, but large result sets may require longer wait times or more processing power.