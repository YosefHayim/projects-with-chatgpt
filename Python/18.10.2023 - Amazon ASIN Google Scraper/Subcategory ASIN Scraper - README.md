# Amazon ASIN Extractor from Google Search

This script automates the extraction of ASINs (Amazon Standard Identification Numbers) from Amazon by first searching for product titles on Google. It is useful for product research and inventory management by gathering ASINs based on product names listed in a CSV file.

## Features

- **Google Search Integration**: Generates Google search URLs for product titles and extracts relevant Amazon links.
- **Amazon Subcategory Navigation**: Navigates Amazon subcategories to find relevant ASINs for each product.
- **CSV Input & Output**: Reads product titles from a CSV file and saves the extracted ASINs into a new CSV file.
- **Chrome Customization**: Disables images and JavaScript for faster page loading and sets the default language to US English.

## Setup

### Prerequisites

- Python 3.x
- Selenium (`pip install selenium`)
- ChromeDriver (ensure it matches your Chrome browser version)

### Installation

1. **Install the required Python packages**:
   ```bash
   pip install selenium
   ```

2. **Download ChromeDriver**:
   Make sure to download the correct version of ChromeDriver that matches your Chrome browser from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

3. **Place ChromeDriver in your PATH**:
   Ensure `chromedriver` is in your system's PATH or specify the path directly in the script.

## Usage

1. **Prepare Your CSV File**:
   Create a CSV file with product titles in the first column, with each title on a separate line.

2. **Run the Script**:
   Start the script by running:
   ```bash
   python amazon_asin_extractor.py
   ```

3. **Input CSV File Path**:
   When prompted, enter the path to your CSV file containing product titles. The script will search Google, extract ASINs from Amazon, and save them to a new CSV file.

4. **ASIN Extraction**:
   The script navigates Amazon subcategories, extracts ASINs, and saves them to a CSV file named after the total number of ASINs found (e.g., `1234 ASINs.csv`). The corresponding ASINs for each title will be displayed in the terminal during processing.

## Script Overview

- **configure_chrome_options**: Configures Chrome options for faster page loads.
- **generate_google_search_url**: Generates Google search URLs based on product titles to find Amazon links.
- **click_last_subcategory**: Clicks the last subcategory on an Amazon page and extracts ASINs from product URLs.
- **CSV Processing**: Reads product titles from a CSV file, processes them, and saves the extracted ASINs into a new CSV file.

## Error Handling

The script includes error handling to manage timeouts, missing files, and navigation errors. If an error occurs, it logs the error and continues processing the next product title.

## Notes

- **Browser Compatibility**: Ensure your ChromeDriver version matches your installed version of Chrome.
- **Google Search**: The script uses Google Search to find relevant Amazon product pages based on the titles in your CSV file.