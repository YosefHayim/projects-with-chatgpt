# eBay Seller Multi-Scraper Script

This Python script automates the process of scraping product titles from multiple eBay seller pages using Selenium and BeautifulSoup. It handles manual CAPTCHA solving and saves the scraped titles into a CSV file.

## Features

- **Incognito Mode**: Browse in incognito mode for privacy.
- **Image-Free**: Disables images to improve page load times.
- **CAPTCHA Detection**: Pauses for manual CAPTCHA solving.
- **Multiple Sellers**: Scrape product titles from multiple sellers in one run.
- **CSV Output**: Saves scraped titles into a CSV file for easy analysis.

## Prerequisites

- Python 3.x
- Selenium (`pip install selenium`)
- LXML (`pip install lxml`)
- ChromeDriver (ensure it matches your Chrome browser version)

## Setup

1. **Install the required Python packages**:
   ```bash
   pip install selenium lxml
   ```

2. **Download ChromeDriver**:
   Download the correct version of ChromeDriver matching your Chrome browser from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

3. **Place ChromeDriver in your PATH**:
   Ensure `chromedriver` is in your system's PATH or specify the path directly in the script.

## Usage

1. **Run the Script**:
   Start the script by running:
   ```bash
   python ebay_seller_scraper.py
   ```

2. **Enter Seller Names**:
   When prompted, type the eBay seller names separated by commas (e.g., `seller1, seller2, seller3`).

3. **Handle CAPTCHAs**:
   If a CAPTCHA appears, the script will pause and prompt you to solve it manually. After solving it, press Enter to continue.

4. **Output**:
   Once the scraping process is complete, the script will generate a CSV file named `SELLERS TITLES <number_of_titles>.csv` containing all the product titles.

## Script Overview

- **setup_browser**: Configures and launches Chrome in incognito mode with images disabled for faster performance.
- **wait_for_element**: Waits for a specific element to appear on the page.
- **click_element**: Clicks on an element after a brief delay, checking for CAPTCHAs.
- **navigate_to_url**: Navigates to the eBay seller's page.
- **interact_with_page**: Sets preferences on the eBay page for optimal scraping.
- **scrape_and_save_data**: Collects product titles and adds them to a list.
- **write_to_csv**: Saves the scraped titles into a CSV file.
- **handle_captcha_manually**: Pauses the script to allow manual CAPTCHA solving.
- **process_seller**: Manages each seller's page, performing interactions and scraping data.

## Error Handling

The script includes error handling for managing timeouts, missing elements, and unexpected issues. If an error occurs, the script will retry up to three times per seller.

## Notes

- **Browser Version Compatibility**: Ensure that your ChromeDriver version matches your installed Chrome version to avoid compatibility issues.
- **Manual Interaction**: CAPTCHA solving requires manual intervention. The script will pause and wait for you to solve the CAPTCHA before continuing.