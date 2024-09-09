from selenium import webdriver
from api_key import config  # Importing the config module where the 2Captcha API key is stored
from selenium.webdriver.chrome.service import Service  # Importing Service class to configure ChromeDriver service
from selenium.webdriver.support.ui import WebDriverWait  # Importing WebDriverWait to wait for elements to load
from selenium.webdriver.support import \
expected_conditions as EC  # Importing EC to use expected conditions for element visibility
from selenium.webdriver.common.by import By  # Importing By to locate elements using different methods (e.g., ID, XPATH)
from twocaptcha import TwoCaptcha  # Importing TwoCaptcha class to interact with 2Captcha API for solving CAPTCHAs
import csv  # Importing CSV module to handle CSV file operations
import time  # Importing time module to handle delays and waiting periods
import os  # Importing OS module to handle file paths and directories
import sys  # Importing sys module to manipulate the Python runtime environment

# Adding the parent directory to the system path to import modules from outside directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def OpenChrome():
    # Define the path to the ChromeDriver executable
    chrome_driver_path = r"C:\Github\Python-Projects\09.08.2024 - Amazon ASIN Collector + normal captcha\Chromedriver\chromedriver.exe"

    # Create a service object with the ChromeDriver path to control the ChromeDriver instance
    service = Service(executable_path=chrome_driver_path)

    # Initialize the Chrome WebDriver with the specified service configuration
    driver = webdriver.Chrome(service=service)

    # Open the Amazon homepage
    driver.get("https://amazon.com")

    # Return the driver object for further use
    return driver


def is_captcha(driver):
    # Check if a specific comment (related to automated access) exists in the body tag of the webpage,
    # which indicates that a CAPTCHA challenge is present.
    if "To discuss automated access to Amazon data please contact api-services-support@amazon.com" in driver.find_element(By.TAG_NAME, "body").get_attribute('innerHTML'):

        # If the comment is found, look for the CAPTCHA image using XPATH
        captcha_img = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, ".//img[contains(@src, 'https://') and contains(@src, '.jpg')]")))

        if captcha_img:
            # Define the path to save the CAPTCHA image
            save_path_img = r"C:\Github\Python-Projects\09.08.2024 - Amazon ASIN Collector + normal captcha\Captcha\captcha_screenshot.png"

            # Take a screenshot of the CAPTCHA image and save it to the specified path
            captcha_img.screenshot(save_path_img)
            return True, save_path_img  # Return True indicating CAPTCHA is detected and provide the image path
    else:
        # If no CAPTCHA is detected, print a message and return False
        print("CAPTCHA not detected.")
        return False, None


def solve_captcha(driver):
    # Retrieve the API key from the config module to authenticate with the 2Captcha service
    api_key = config.API_KEY_2CAPTCHA
    solver = TwoCaptcha(api_key)  # Initialize the TwoCaptcha solver object with the API key

    captcha_solved = False  # Initialize a flag to track if the CAPTCHA is solved

    while not captcha_solved:  # Loop until the CAPTCHA is successfully solved
        # Refresh the CAPTCHA image by calling is_captcha again to get the latest CAPTCHA image
        captcha_detected, captcha_image_path = is_captcha(driver)

        if captcha_detected:
            # Send the CAPTCHA image to 2Captcha API and retrieve the solved code
            result = solver.normal(captcha_image_path)
            print('Normal Captcha Provided:', result)

            # Locate the CAPTCHA input field on the webpage using its ID
            captcha_input_field = driver.find_element(By.ID, "captchacharacters")

            # Input the solved CAPTCHA code into the CAPTCHA input field
            captcha_input_field.send_keys(result['code'])

            # Locate and click the submit button to submit the CAPTCHA solution
            continue_shopping_button = driver.find_element(By.CLASS_NAME, "a-button-text")
            continue_shopping_button.click()

            # Wait for 5 seconds to allow the page to reload and check if the CAPTCHA is still present
            time.sleep(5)

            try:
                # Attempt to locate the CAPTCHA input field again to determine if the CAPTCHA was not solved
                driver.find_element(By.ID, "captchacharacters")
                print(
                    "CAPTCHA was not solved correctly, trying again...")  # Print message indicating CAPTCHA was not solved
            except:
                # If CAPTCHA input field is not found, assume CAPTCHA is solved successfully
                print("CAPTCHA solved successfully.")
                captcha_solved = True  # Set the flag to True to exit the loop
        else:
            # If no CAPTCHA is detected on retry, print a message and exit the loop
            print("No CAPTCHA detected on retry, continuing with the process.")
            captcha_solved = True  # Set the flag to True to exit the loop


def zipcode_change(driver):
    # Step 1: Locate and click the element (ID: nav-global-location-data-modal-action) to open the location change modal
    location_modal = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "nav-global-location-data-modal-action")))
    location_modal.click()

    time.sleep(1)  # Wait for 1 second to ensure the modal is fully loaded

    # Step 3: Locate the ZIP code input field (Class: GLUX_Full_Width) within the modal and input the ZIP code "33180"
    zip_input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "GLUX_Full_Width")))
    zip_input_field.send_keys("33180")

    # Step 4: Locate and click the submit button (XPATH: //input[@aria-labelledby='GLUXZipUpdate-announce']) to update the ZIP code
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-labelledby='GLUXZipUpdate-announce']")))
    submit_button.click()

    time.sleep(2)  # Wait for 2 seconds to allow the ZIP code change to process

    # Step 5: Locate and click the close button (XPATH: //button[@data-action='a-popover-close' and @aria-label='Close']) to close the modal
    close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-action='a-popover-close' and @aria-label='Close']")))
    close_button.click()


def search_and_type(driver):
    # Step 1: Locate the Amazon search input box (ID: twotabsearchtextbox)
    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))

    # Step 2: Click on the search input box to focus it
    search_box.click()

    # Step 3: Wait for the user to input a search term; prompt until valid input is provided
    while True:
        user_input = input("Please enter the search term for Amazon: ")

        if user_input.strip():  # If the input is not empty or whitespace, break out of the loop
            break
        else:
            print("Input cannot be empty. Please enter a valid search term.")

    # Step 4: Type the user-provided input into the search box
    search_box.send_keys(user_input)

    # Step 5: Locate and click the search submit button (ID: nav-search-submit-button) to perform the search
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button")))
    submit_button.click()

    return user_input  # Return the search term for further use


def getPagesInfoAndNavigate(driver, search_term):
    found_asins = set()  # Initialize an empty set to store unique ASINs
    total_asins_count = 0  # Counter to keep track of the total number of ASINs found
    total_pages = 0  # Variable to store the total number of pages in the search results
    current_url = ""  # Variable to store the current URL for resuming in case of an interruption

    try:
        # Get the total number of pages from the search results
        total_pages_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='s-pagination-item s-pagination-disabled' and @aria-disabled='true']")))
        total_pages = int(total_pages_element.text)  # Convert the total pages to an integer
        print(f"Total pages: {total_pages}")

        while True:
            # Save the current page's URL to memory for resuming in case of a failure
            current_url = driver.current_url

            # Check if CAPTCHA is present on the page and solve it if detected
            captcha_detected, captcha_image_path = is_captcha(driver)
            if captcha_detected:
                solve_captcha(driver)
                # After solving the CAPTCHA, reload the last saved URL
                driver.get(current_url)
                time.sleep(3)  # Allow some time for the page to load after solving CAPTCHA

                # Re-check for CAPTCHA after reloading the page
                captcha_detected, captcha_image_path = is_captcha(driver)
                if captcha_detected:
                    print("CAPTCHA detected again after solving, trying again...")
                    solve_captcha(driver)
                    driver.get(current_url)
                    time.sleep(3)

            # Get the current page number by locating the selected pagination element
            current_page_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='s-pagination-item s-pagination-selected']")))
            current_page = int(current_page_element.text)  # Convert the current page number to an integer

            print(f"Current page: {current_page}/{total_pages}")

            # Locate all product elements on the page containing ASINs
            product_elements = driver.find_elements(By.XPATH, "//div[@data-asin and @data-index]")

            page_asins_count = 0  # Counter to keep track of the number of ASINs found on the current page
            for product in product_elements:

                asin = product.get_attribute("data-asin")  # Extract the ASIN from each product element
                if asin and asin not in found_asins:  # Ensure the ASIN is unique and not already found
                    found_asins.add(asin)  # Add the unique ASIN to the set
                    total_asins_count += 1  # Increment the total ASIN count
                    page_asins_count += 1  # Increment the page-specific ASIN count

            print(f"ASINs found on page {current_page}: {page_asins_count}")
            print(f"Total ASINs found so far: {total_asins_count}")

            # Check if the current page is the last page
            if current_page < total_pages:
                # Locate and click the "Next" button to navigate to the next page of results
                next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 's-pagination-next')]")))
                next_button.click()

                print(f"Navigating to the next page: {current_page + 1}")
            else:
                print("Reached the last page.")
                break  # Exit the loop when the last page is reached

    except Exception as e:
        # Catch any exceptions that occur during the process
        print(f"An error occurred: {e}")
        if current_url:
            
            # If an error occurs and the current URL is saved, reload it to retry
            print(f"Reloading last URL due to error: {current_url}")
            driver.get(current_url)
            time.sleep(3)  # Allow some time for the page to load after reload

    finally:
        # Save the collected ASINs to a CSV file, even if an error occurs
        directory = r"C:\Github\Python-Projects\09.08.2024 - Amazon ASIN Collector + normal captcha\History"
        # Sanitize the search term to create a safe file name
        sanitized_search_term = "".join([c for c in search_term if c.isalnum() or c in (' ', '_')]).rstrip()
        csv_filename = os.path.join(directory, f"{sanitized_search_term} - {total_asins_count} - ASINS.csv")

        with open(csv_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for asin in found_asins:
                writer.writerow([asin])  # Write each ASIN to the CSV file

        print(f"ASINs have been saved to {csv_filename}")
        if total_pages and current_page == total_pages:
            print("Successfully finished all pages.")


def main():
    driver = OpenChrome()  # Open the Chrome browser and navigate to Amazon

    try:
        # Check if CAPTCHA is present on the homepage
        captcha_detected, captcha_image_path = is_captcha(driver)

        if captcha_detected:
            # If a CAPTCHA is detected, solve it before proceeding
            solve_captcha(driver)
            time.sleep(4)  # Allow some time for the page to load after solving CAPTCHA

        # Proceed with changing the ZIP code, searching for the product, and collecting ASINs
        zipcode_change(driver)
        time.sleep(6)
        search_term = search_and_type(driver)
        getPagesInfoAndNavigate(driver, search_term)

    except Exception as e:
        # Catch any exceptions that occur during the execution
        print(f"An error occurred: {e}")
    finally:
        # Ensure that the browser is closed properly after the script is done
        driver.quit()


main()  # Execute the main function to start the script
