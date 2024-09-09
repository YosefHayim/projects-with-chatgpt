from selenium import webdriver
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import \
expected_conditions as EC 
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import NoSuchElementException
import csv 
import time 
import os 
import sys 

#Setting the file first so it can append each loop the titles

# Setting the chrome browser
service = Service(executable_path=r"C:\Github\Python-Projects\11.08.2024 - eBay Titles Scraper\Chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    # Get to the url
    driver.get('https://www.ebay.com')

    # wait for the elements to load
    time.sleep(2)

    # Locating the search bar input and clicking on it
    search_box = driver.find_element(By.XPATH, "//*[@aria-label='Search for anything']")
    search_box.click()

    # sending text to input and clicking enter
    search_term = input('What would you like to search and fetch from eBay?')
    search_box.send_keys(search_term + Keys.ENTER)

    time.sleep(2)

    # change items to 240 per page
    items_per_page_element = driver.find_element(By.XPATH, '//*[@id="srp-ipp-menu"]/button/span')
    # Clicking on the element
    items_per_page_element.click()

    change_items_to_240 = driver.find_element(By.XPATH, f"//a[@href='https://www.ebay.com/sch/i.html?_from=R40&_nkw={search_term}&_sacat=0&_ipg=240']")
    change_items_to_240.click()
    print('Changed to 240 items per page view')

    time.sleep(4)

    # From here the loop starts to iterate over each page

    # We first set page number to 1 because on eBay we always start from 1
    current_page_number = 1
    # List to store the titles on each loop
    product_titles_storage = []
    # Counting the products on each loop
    count_products = 0

    while True:
        #Get current page location:
        current_page_text = driver.find_element(By.CLASS_NAME, 'pagination__item').text

        # Get Total search results for the search term
        Total_results_found = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@class="srp-controls__count-heading"]/span[1]'))).text

        # get all the products titles on page
        product_titles_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@role='heading']")))

        for i in product_titles_elements:
        # On each loop append the current title being fetched
            product_titles_storage.append(i.text)
            count_products += 1

        print(f'Page: {current_page_number}\nTotal Titles Found:{count_products}')
        # Return them all to the list when the all iterations when the loop is over.

        try:
            # Before clicking on the next page we modify the current page in the element url so we click on it.
            current_page_number += 1

            # Next button element and clicking on it
            next_button = driver.find_element(By.XPATH, f"//a[@href='https://www.ebay.com/sch/i.html?_from=R40&_nkw={search_term}&_sacat=0&_ipg=240&_pgn={current_page_number}']")
            next_button.click()

            time.sleep(3)

        except NoSuchElementException:
            print(f"No more pages to scrape, reached the last page {NoSuchElementException}")
            break
# If from anyreason the script is crashing or something has happend then the data is exported right away to the history folder.
finally:
    History_folder = r"C:\Github\Python-Projects\11.08.2024 - eBay Titles Scraper\History"

    # filename with the product count
    filename = f'{search_term} - {count_products} titles.csv'
    
    # Create the full path by joining the directory and filename
    full_path = os.path.join(History_folder, filename)

    # Writing all collected titles to the CSV file
    with open(full_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Writing the header
        writer.writerow(['Title'])  
        for title in product_titles_storage:
            # Writing each title to a new row
            writer.writerow([title])  


    print(f'All titles have been written to {full_path}')

