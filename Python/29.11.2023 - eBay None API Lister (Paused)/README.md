# Amazon Product Data Scraper

This Python script automates the extraction of detailed product information from Amazon using Selenium. It gathers data such as images, prices, categories, and more, making it ideal for product research.

## Features

- **Cookie Management**: Saves and loads cookies to maintain session continuity.
- **Data Cleaning**: Cleans text data by removing unwanted characters.
- **CSV Handling**: Reads ASINs from a CSV file and exports product data back to a CSV file.
- **Blacklist Support**: Skips blacklisted ASINs.
- **Image Scraping**: Retrieves high-resolution images from product pages.
- **Detailed Extraction**: Captures a wide range of product details including brand, title, price, category, etc.

## Prerequisites

- Python 3.x
- Selenium (`pip install selenium`)
- LXML (`pip install lxml`)
- ChromeDriver (ensure it matches your Chrome browser version)

## Setup

1. **Install the required packages**:
   ```bash
   pip install selenium lxml
   ```

2. **Download ChromeDriver**:
   Download the correct version of ChromeDriver matching your Chrome browser from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

3. **Place ChromeDriver in your PATH**:
   Ensure `chromedriver` is in your system's PATH or specify the path directly in the script.

## Usage

1. **Run the Script**:
   ```bash
   python amazon_scraper.py
   ```

2. **Input the ASINs CSV File**:
   The script reads ASINs from a CSV file named `ASINS_EXTRACTION.csv`. Ensure this file is in the same directory as the script or provide the full path.

3. **Manual Actions**:
   Perform any manual actions needed (e.g., logging in) once the browser opens. Press Enter in the terminal to continue the script.

4. **Script Execution**:
   The script will process each ASIN, gather product data, and save it into a CSV file named `DATA_EXPORTED.csv`.

5. **Output**:
   After the script finishes, you’ll have a CSV file with organized product data ready for analysis.

## Script Overview

- **save_cookies & load_cookies**: Manages session cookies.
- **clean_text**: Normalizes text data.
- **read_asins_from_csv**: Reads ASINs for processing.
- **is_blacklisted**: Skips blacklisted ASINs.
- **fetch_product_data**: Extracts product information from Amazon.
- **main**: Orchestrates the process from cookie management to data extraction and CSV export.

## Error Handling

The script includes error handling for issues like missing elements, timeouts, and unexpected errors. Detailed error logs help diagnose issues quickly.

## Notes

- **Browser Compatibility**: Ensure your ChromeDriver version matches your Chrome browser.
- **High-Resolution Images**: The script retrieves high-resolution images from product pages.