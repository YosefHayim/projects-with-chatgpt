# Multi-Browser Amazon ASIN Scraper

This advanced script uses multiprocessing to scrape ASINs (Amazon Standard Identification Numbers) from Amazon more efficiently by distributing the workload across multiple browser instances. It retrieves ASINs based on product titles from a CSV file and automates the process using Selenium.

## Features

- **Multi-Browser Processing**: Distributes scraping tasks across multiple browser instances for improved speed.
- **Google Search Integration**: Searches Google for product titles and extracts relevant Amazon ASINs.
- **CSV Input & Output**: Reads product titles from a CSV file and saves extracted ASINs into a new CSV file.
- **Custom Chrome Options**: Configures Chrome with optimized settings such as incognito mode and disabled extensions.

## Setup

### Prerequisites

- Python 3.x
- Selenium (`pip install selenium`)
- ChromeDriver (ensure it matches your Chrome browser version)
- Multiprocessing support (available in Python by default)

### Installation

1. **Install the required Python packages**:
   ```bash
   pip install selenium
   ```

2. **Download ChromeDriver**:
   Download the correct version of ChromeDriver matching your Chrome browser from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

3. **Place ChromeDriver in your PATH**:
   Ensure `chromedriver` is in your system's PATH or specify the path directly in the script.

## Usage

1. **Prepare Your CSV File**:
   Create a CSV file with product titles in the first column, each on a separate line.

2. **Run the Script**:
   Start the script by running:
   ```bash
   python multi_browser_asin_scraper.py
   ```

3. **Input CSV File Path and Number of Browsers**:
   When prompted, enter the path to your CSV file and specify the number of browser instances for parallel processing.

4. **ASIN Extraction**:
   The script launches multiple browser instances, searches Google for each product title, extracts ASINs from Amazon links, and saves them to a CSV file named after the total ASINs found (e.g., `1234 ASINs.csv`).

## Script Overview

- **start_multiprocessing**: Distributes tasks across multiple browser instances for parallel processing.
- **navigate_to_google_and_search**: Searches Google for product titles and extracts ASINs from Amazon links.
- **CSV Processing**: Reads product titles from a CSV file and saves extracted ASINs into a new CSV file.
- **setup_browser**: Configures Chrome with optimized options for improved performance.

## Error Handling

The script includes error handling for issues like timeouts or navigation errors. If an error occurs, it logs the error and continues processing the next title.

## Notes

- **Browser Compatibility**: Ensure your ChromeDriver version matches your installed version of Chrome.
- **Multiprocessing Efficiency**: Choose the number of browser instances based on your system's capabilities to avoid slowing down the process or causing instability.