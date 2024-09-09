# Amazon ASIN Collector with CAPTCHA Solver

## Overview

This Python script automates the collection of ASINs (Amazon Standard Identification Numbers) from Amazon search results using Selenium. It can handle CAPTCHA challenges with the 2Captcha service, change the ZIP code, and export the collected ASINs to a CSV file.

## Requirements

- Python 3.x
- Selenium
- 2Captcha API key
- Chrome WebDriver (compatible with your Chrome version)
- `twocaptcha-python` package

## Setup

1. Install the required Python packages:

   ```bash
   pip install selenium twocaptcha-python
   ```

2. Download and place the Chrome WebDriver in the specified path:

   ```
   C:\Github\Python-Projects\09.08.2024 - Amazon ASIN Collector + normal captcha\Chromedriver\chromedriver.exe
   ```

3. Add your 2Captcha API key to the `api_key.py` file:
   ```python
   # api_key.py
   API_KEY_2CAPTCHA = 'your_2captcha_api_key'
   ```

## Usage

1. Run the script:

   ```bash
   python amazon_asin_collector.py
   ```

2. The script will:

   - Open Amazon in Chrome.
   - Solve CAPTCHA challenges if detected.
   - Change the ZIP code.
   - Prompt for a search term.
   - Collect ASINs from search results across multiple pages.

3. The collected ASINs will be saved in a CSV file in the `History` folder:
   ```
   C:\Github\Python-Projects\09.08.2024 - Amazon ASIN Collector + normal captcha\History
   ```

## Output

- The ASINs are saved in a CSV file named `{search_term} - {total_asins_count} - ASINS.csv` in the `History` folder.

## Error Handling

- The script solves CAPTCHAs automatically using the 2Captcha service.
- If an error occurs, the collected ASINs are saved up to that point.
- The browser closes automatically when the script completes.

## Notes

- Ensure the Chrome WebDriver is compatible with your Chrome version.
- Provide your 2Captcha API key in the `api_key.py` file.
