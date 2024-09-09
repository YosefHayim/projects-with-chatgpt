from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process, Manager
import csv
import re
import os
import math


def start_multiprocessing(all_titles, num_browsers):
    """Distributes the workload across multiple browser instances."""
    manager = Manager()
    extracted_ids = manager.list()

    num_titles = len(all_titles)
    titles_per_browser = num_titles // num_browsers
    extra_titles = num_titles % num_browsers

    processes = []
    start = 0

    for i in range(1, num_browsers + 1):
        end = start + titles_per_browser + (1 if extra_titles > 0 else 0)
        subset_of_titles = all_titles[start:end]
        p = Process(target=process_titles, args=(subset_of_titles, extracted_ids, i))
        p.start()
        processes.append(p)
        start = end
        extra_titles -= 1

    for p in processes:
        p.join()

    return list(extracted_ids)

def process_titles(subset_of_titles, extracted_ids, browser_number):
    """Processes a subset of titles in a separate browser."""
    driver = setup_browser()
    total_titles = len(subset_of_titles)
    print(f"\nBrowser {browser_number} starting to process {total_titles} titles.\n")

    for idx, title in enumerate(subset_of_titles):
        navigate_to_google_and_search(driver, title, extracted_ids, idx, total_titles, browser_number)

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--headless")  # Comment out or remove this line to make the browser visible
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]


def write_asins_to_csv(asins):
    file_name = f"{len(asins)} ASINs.csv"
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ASINs"])
        for asin in asins:
            writer.writerow([asin])


def extract_specific_text_from_url(url):
    pattern = re.compile(r'/dp/([A-Z0-9]{10})')
    match = pattern.search(url)
    return match.group(1) if match else None


def navigate_to_google_and_search(driver, title, extracted_ids_set, idx, total_titles, browser_number):
    if idx == 0:
        driver.get("https://www.google.com/")
        search_box = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "q")))
    else:
        search_box = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()

    search_box.send_keys(title)
    search_box.submit()

    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a')))

    amazon_links = [a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, 'a') if
                    a.get_attribute('href') and "amazon" in a.get_attribute('href')][:5]

    asins_for_current_title = set()
    for amazon_url in amazon_links:
        extracted_text = extract_specific_text_from_url(amazon_url)
        if extracted_text:
            asins_for_current_title.add(extracted_text)

    # Append unique ASINs to the shared list
    for asin in asins_for_current_title:
        if asin not in extracted_ids_set:
            extracted_ids_set.append(asin)

    print(f"\nRobotScarper {browser_number} - Title {idx + 1}/{total_titles} 📚 - ASINs: {' '.join(asins_for_current_title)} 🚀\n")


def main():
    csv_file_location = input("Please enter the full path to your titles CSV file: \n").strip("\"")
    num_browsers = int(input("\nPlease enter the number of browsers to open: \n").strip())

    if not os.path.exists(csv_file_location):
        print(f"File does not exist at path: {csv_file_location}. Exiting.")
        return

    titles = read_csv(csv_file_location)
    extracted_ids = start_multiprocessing(titles, num_browsers)

    # Remove duplicates by converting the list to a set and back to a list
    unique_extracted_ids = list(set(extracted_ids))

    write_asins_to_csv(unique_extracted_ids)


if __name__ == "__main__":
    main()