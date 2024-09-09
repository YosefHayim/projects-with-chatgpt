# eBay API Draft Listing Script (Currently Paused)

This script was designed to automate the creation of draft listings on eBay using their API. However, the project is currently paused due to issues with obtaining approval from the eBay Developer Program.

## Project Overview

The script aims to streamline the process of creating eBay draft listings by interacting directly with the eBay API.

- **OAuth Authentication**: Secures an OAuth token to authenticate API requests.
- **Draft Listings**: Automates the creation of draft product listings with customizable details (title, description, images, pricing).
- **JSON Payload**: Uses a structured JSON payload to define product attributes.

## Project Status: Paused

The project is on hold due to a denial of API access from the eBay Developer Program. Without API approval, the script cannot be fully tested or deployed. Future development will resume once access issues are resolved.

## Script Overview

- **get_oauth_token**: Handles OAuth 2.0 authentication to obtain an access token.
- **create_draft_listing**: Sends a POST request to the eBay API to create a draft listing.
- **main**: Orchestrates the process by obtaining the access token and attempting to create a draft listing.

## Setup

To explore or attempt running the script in a sandbox environment:

1. **Install the required packages**:
   ```bash
   pip install requests
   ```
2. **Replace API Credentials**: Add your `CLIENT_ID` and `CLIENT_SECRET` if you have eBay API credentials.
3. **Run the Script**:
   ```bash
   python ebay_api_script.py
   ```

## Prerequisites

- Python 3.x
- eBay Developer Program Account (Sandbox access)

## Important Note

The script may not function as intended without proper API access. For more information on applying for API access, visit the [eBay Developer Program](https://developer.ebay.com/).

## Future Plans

- **Reapply for API Access**: Attempt to gain eBay API approval.
- **Further Development**: Add more features once API access is granted.