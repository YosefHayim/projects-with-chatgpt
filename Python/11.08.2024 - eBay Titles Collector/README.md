# eBay Titles Scraper

## Overview

This Python script automates the process of scraping product titles from eBay search results using Selenium. It navigates through multiple pages and saves the collected titles in a CSV file.

## Requirements

- Python 3.x
- Selenium
- Chrome WebDriver (compatible with your Chrome version)

## Setup

1. Install the required Python package:
   ```bash
   pip install selenium
   ```
2. Download and place the Chrome WebDriver in the specified path:
   ```
   C:\Github\Python-Projects\11.08.2024 - eBay Titles Scraper\Chromedriver\chromedriver.exe
   ```

## Usage

1. Set the search term in the script (`search_term = 'hats'`).
2. Run the script:
   ```bash
   python ebay_titles_scraper.py
   ```
3. The script will:
   - Open eBay and perform the search.
   - Scrape product titles from multiple pages.
   - Save the titles to a CSV file in the `History` folder:
     ```
     C:\Github\Python-Projects\11.08.2024 - eBay Titles Scraper\History
     ```

## Output

- The titles are saved in a CSV file named `{search_term} - {count_products} titles.csv` in the `History` folder.
- The CSV file includes a `Title` column listing all the scraped titles.

## Error Handling

- If the script encounters an error or finishes scraping all pages, it automatically exports the collected titles to the CSV file.

## Notes

- Ensure the Chrome WebDriver is compatible with your Chrome version.
- Adjust the search term and file paths in the script as needed.