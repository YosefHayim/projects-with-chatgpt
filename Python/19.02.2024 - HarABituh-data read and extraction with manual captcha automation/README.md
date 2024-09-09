# Selenium Automation Script

This script automates interactions with a website using Selenium WebDriver and Python. It handles login, navigation, web element interaction, and data extraction from an Excel file to input into the website.

## Features

- **Automated Browser Interaction**: Opens Chrome in incognito mode and performs actions.
- **Login Automation**: Handles login, including two-factor authentication.
- **Excel Integration**: Reads data from an Excel file for form filling.
- **Date Handling**: Extracts and formats dates from Excel, selecting the correct date on the website.
- **JavaScript Execution**: Executes JavaScript to interact with elements.
- **CAPTCHA Handling**: Pauses for user input during CAPTCHA challenges.

## Libraries Used

- **Selenium**
- **WebDriver Manager**
- **OpenPyXL**

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/selenium-automation-script.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd selenium-automation-script
   ```
3. **Install Required Libraries**:
   ```bash
   pip install selenium webdriver-manager openpyxl
   ```
4. **Prepare the Excel File**: Ensure `Test_fill.xlsx` is in the correct directory and contains the necessary IDs and dates.
5. **Check Chrome Installation**: Ensure you have the latest version of Chrome installed.

## Usage Instructions

1. **Run the Script**:
   ```bash
   python automation_script.py
   ```
2. **Follow the Prompts**: Enter CAPTCHA codes and two-factor authentication as needed.
3. **Wait for Completion**: The script will handle all necessary interactions and form submissions.
4. **Excel Output**: The script will download data into an Excel file as part of its process.

## Project Structure

```plaintext
selenium-automation-script/
├── automation_script.py   # Main script file
├── README.md              # This README file
└── Test_fill.xlsx         # Excel file containing input data
```

## Troubleshooting

- **Element Not Found**: Ensure the website structure has not changed. Verify that the selectors in the script match the website's HTML.
- **CAPTCHA Handling**: Double-check your CAPTCHA input.
- **WebDriver Errors**: Ensure your ChromeDriver version matches your Chrome version.