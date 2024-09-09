# Amazon ASINS Scraper

This project is an automated script for interacting with Amazon, solving CAPTCHA challenges, applying user-defined filters, and scraping ASINs from search results. It uses [Puppeteer](https://github.com/puppeteer/puppeteer) for browser automation and [2captcha API](https://github.com/infosimples/node_two_captcha) to solve CAPTCHAs.

## Features

- **CAPTCHA Handling**: Detects and solves CAPTCHAs on Amazon using the 2captcha API.
- **ZIP Code Automation**: Automatically enters and submits a ZIP code to customize content based on location.
- **User Input Filters**: Allows users to apply filters such as star ratings, price ranges, and coupons during ASIN scraping.
- **ASIN Extraction**: Scrapes unique ASINs from search results across multiple pages.
- **Pagination**: Automatically navigates through multiple pages of results.
- **CSV Export**: Saves the extracted ASINs to a CSV file.

## Prerequisites

- Node.js
- Puppeteer (`npm install puppeteer`)
- 2captcha API key ([Get it from 2captcha](https://2captcha.com))

## Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   npm install puppeteer @infosimples/node_two_captcha
   ```
3. Add your 2captcha API key to the script.

## Usage

- **getAmazon**: Navigates to Amazon's homepage and prepares for further actions.
- **isCaptcha**: Detects CAPTCHAs and retrieves the CAPTCHA image URL if present.
- **solveCaptcha**: Solves the CAPTCHA using the 2captcha API and submits the solution.
- **zipcodeChange**: Automates the process of entering a ZIP code on Amazon.
- **searchTermByUser**: Prompts the user for a search term and applies filters.
- **extractASINS**: Scrapes unique ASINs from the search results.
- **goNextPage**: Handles pagination and tracks progress through search result pages.
- **saveAsinsToCSV**: Saves the extracted ASINs to a CSV file.
- **userFilters**: Applies user-defined filters such as star ratings, price range, and coupons.
- **findAsinsWithCoupons**: Specifically extracts ASINs that have available coupons.