# Amazon Outlet Deals ASIN Scraper

This script is designed to help you efficiently scrape ASINs (Amazon Standard Identification Numbers) from Amazon's outlet deals page. It's a valuable tool for gathering product information or analyzing discounts on Amazon.

## Features

- **Advanced Filtering**: Automatically applies filters like categories, deals, discounts, and ratings to narrow down search results.
- **Pagination Handling**: Seamlessly navigates through multiple pages of Amazon deals to capture all relevant ASINs.
- **CSV Export**: Saves the extracted ASINs into a CSV file for easy analysis and integration with other applications.

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
   python amazon_outlet_deals_scraper.py
   ```

2. **Automatic Filtering**:
   The script will automatically apply filters such as categories, deals, discounts, and ratings to narrow down the results.

3. **ASIN Extraction**:
   The script will navigate through all available pages on the Amazon Outlet Deals page, extracting ASINs as it goes.

4. **CSV Export**:
   After scraping, the extracted ASINs will be saved into a CSV file named after the total number of ASINs found (e.g., `123_asins.csv`). The file will be saved in your current directory.

## Script Overview

- **initialize_webdriver**: Sets up the Chrome browser and navigates to the Amazon Outlet Deals URL.
- **apply_filters**: Applies various filters, including categories, deals, discounts, and ratings.
- **navigate_to_next_page**: Clicks the "Next" button to navigate through multiple pages of results.
- **extract_asins**: Uses BeautifulSoup to parse HTML content and extract ASINs from product links.
- **export_to_csv**: Saves the extracted ASINs to a CSV file.

## Error Handling

The script includes error handling to manage issues such as timeouts, missing elements, or navigation errors. If an error occurs, the script will log the error and continue processing the next page.

## Notes

- **Browser Compatibility**: Ensure that your ChromeDriver version matches your installed Chrome browser version to avoid compatibility issues.
- **Dynamic Content**: The script is designed to handle dynamic content, but large result sets may require longer wait times or additional processing power.