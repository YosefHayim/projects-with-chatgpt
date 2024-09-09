# Amazon ASIN Scraper

This script automates the process of extracting ASINs (Amazon Standard Identification Numbers) from Amazon search results using Selenium and BeautifulSoup. It is designed to efficiently gather product data for analysis or business use.

## Features

- **Dynamic Scrolling**: Automatically scrolls through Amazon search result pages to load and capture dynamic content.
- **ZIP Code Customization**: Changes the delivery location to a specified ZIP code for localized search results.
- **Search Term Flexibility**: Accepts multiple search terms, processing each one separately to extract ASINs.
- **CSV Export**: Saves all extracted ASINs into a CSV file for easy analysis.

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
   Download the correct version of ChromeDriver matching your Chrome browser from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

3. **Place ChromeDriver in your PATH**:
   Ensure `chromedriver` is in your system's PATH or specify the path directly in the script.

## Usage

1. **Run the Script**:
   Start the script by running:
   ```bash
   python amazon_asin_scraper.py
   ```

2. **Input Search Terms**:
   When prompted, enter search terms separated by commas (e.g., `laptop, phone case, bluetooth speaker`). The script will process each term individually.

3. **ZIP Code Customization**:
   The script automatically changes the delivery location to ZIP code `33180`. Modify this in the script if you need a different location.

4. **ASIN Extraction**:
   The script scrolls through search results pages, extracts ASINs, and saves them to a CSV file named after the total number of ASINs found (e.g., `1234 ASINS.csv`).

## Script Overview

- **initialize_webdriver**: Sets up a Chrome browser with incognito mode and disabled images for faster loading.
- **scroll_page**: Scrolls through Amazon search results pages to load dynamic content.
- **change_zip_code**: Changes the Amazon delivery location to the specified ZIP code.
- **get_search_terms**: Prompts the user to input search terms, which are then split into a list for processing.
- **get_asins_on_page**: Extracts ASINs from the current page using BeautifulSoup.
- **navigate_to_next_page**: Navigates to the next page of search results.
- **save_asins_to_csv**: Saves the extracted ASINs to a CSV file.

## Error Handling

The script includes error handling to manage issues like timeouts or missing elements. If an error occurs, it will log the error and continue processing the next search term.

## Customization

- **ZIP Code**: Change the ZIP code in the `change_zip_code` function to customize the delivery location.
- **Scroll Settings**: Adjust the number of scrolls and the sleep time between them in the `scroll_page` function to control content loading.

## Notes

- Ensure your ChromeDriver version matches your installed version of Chrome to avoid compatibility issues.
- The script is designed to handle dynamic content, but large result sets may require longer wait times or additional scrolls.