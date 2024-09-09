import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl

chrome_options = Options()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get('https://login.gov.il/nidp/saml2/sso?id=usernamePasswordSMSOtp&sid=2&option=credential&sid=2')

try:
    # Wait for the userId input box to be available (visible on the page)
    input_box_id = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "userId"))
    )
    # Type the desired value (ID Number) into the input box
    input_box_id.send_keys('ID Number')
except Exception as e:
    print("Element not found or another error occurred:", e)

try:
    # Wait for the userPass input box to be available
    input_box_pw = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "userPass"))
    )
    # Type the desired value (Password) into the input box
    input_box_pw.send_keys('ID Password')
except Exception as e:
    print("Element not found or another error occurred:", e)

# Click the login button
login_button_click = driver.find_element(By.CLASS_NAME, "submit-button_label_container_icon__xjv7L")
login_button_click.click()

# Pause the script and wait for the user to input the email code
wait_for_2_authn = input('Reply once you have entered the 6-digit email code.\n')

# Navigate to the next page
time.sleep(1)
driver.get('https://harb.cma.gov.il/sso/Overview')
time.sleep(1)

# Pause the script and wait for the user to click certain buttons
wait2_for_2_authn = input('Reply once you clicked the X and clicked on the blue button.\n')

# Wait time of 3 seconds
clicking_entering_extra_file_button = 3

# Wait for the button to be clickable, then click it
button_element = WebDriverWait(driver, clicking_entering_extra_file_button).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-bs-target='#moreInsurance']"))
)
button_element.click()

# Wait time of 3 seconds
clicking_childs_name_bithuaim_tik = 3

# Wait for the next button to be clickable, then click it
button_element = WebDriverWait(driver, clicking_childs_name_bithuaim_tik).until(
    EC.element_to_be_clickable((By.ID, "butFindChild"))
)
button_element.click()

print("3: COPY & PASTE ID FROM COLUMN A\n")

# Wait for 2 seconds
time.sleep(2)

# Wait for the input element to be ready
try:
    id_input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "txtId"))
    )
except Exception as e:
    print(f"Error finding input element: {e}")
    driver.quit()

# File path to the Excel file
file_path = "C:\\Users\\User\\PycharmProjects\\pythonProject\\Kedmi Bithuaim - Automation Har Abituah\\Test_fill.xlsx"

try:
    # Load the Excel file
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet = wb.active
    id_value = sheet['A1'].value  # Get the ID from the first cell in column A

    if id_value is not None:
        id_input_element.clear()  # Clear any pre-existing text in the input box
        id_input_element.send_keys(str(id_value))  # Type the ID into the input box

        print(f"ID being processed: {id_value}")
    else:
        print("No ID value found in the Excel file.")
except Exception as e:
    print(f"Error reading Excel file: {e}")

# Extract and format the date from Excel
date_value = sheet['B1'].value  # Get the date from the first cell in column B

if date_value is not None:
    # Split the date into day, month, and year components
    day, month, year = date_value.strftime("%d/%m/%Y").split('/')
    print(f"Extracted Date: Day: {day}, Month: {month}, Year: {year}")
else:
    print("No date value found in the Excel file.")
    driver.quit()

# Day selection using a dropdown menu
try:
    dropdown_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".k-dropdown-wrap.k-state-default"))
    )
    dropdown_element.click()
except Exception as e:
    print(f"Error clicking the dropdown: {e}")

# Execute JavaScript to select the day
try:
    js_command = f"""
    var day = "{day}";
    var optionsList = document.getElementById('uiDdlDay_listbox').querySelectorAll('li');
    var optionToClick = Array.from(optionsList).find(li => li.textContent.includes(day));
    if (optionToClick) optionToClick.click();
    """
    driver.execute_script(js_command)
except Exception as e:
    print(f"Could not select the day using JavaScript: {e}")

# Month selection using a dropdown menu
try:
    month_dropdown_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".uiDdlMonth .k-dropdown-wrap.k-state-default"))
    )
    month_dropdown_element.click()
except Exception as e:
    print(f"Error clicking the month dropdown: {e}")

month_int = int(month)  # Convert the month string to an integer

# Execute JavaScript to select the month
try:
    js_command = f"""
    var month = {month_int};
    var optionsList = document.getElementById('uiDdlMonth_listbox').querySelectorAll('li');
    var optionToClick = Array.from(optionsList).find(li => parseInt(li.textContent) === month);
    if (optionToClick) optionToClick.click();
    """
    driver.execute_script(js_command)
except Exception as e:
    print(f"Could not select the month using JavaScript: {e}")

# Year selection using a dropdown menu
try:
    year_dropdown_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".uiDdlYear .k-dropdown-wrap.k-state-default"))
    )
    year_dropdown_element.click()
except Exception as e:
    print(f"Error clicking the year dropdown: {e}")

# Execute JavaScript to select the year
try:
    js_command = f"""
    var year = "{year}";
    var optionsList = document.getElementById('uiDdlYear_listbox').querySelectorAll('li');
    var optionToClick = Array.from(optionsList).find(li => li.textContent.includes(year));
    if (optionToClick) optionToClick.click();
    """
    driver.execute_script(js_command)
except Exception as e:
    print(f"Could not select the year using JavaScript: {e}")

# CAPTCHA input
try:
    captcha_input_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "CaptchaCode"))
    )
    # Ask the user to input the CAPTCHA code
    what_is_code = input('What is the CAPTCHA code you see in the browser?')
    captcha_input_element.send_keys(what_is_code)
    print(f"CAPTCHA code {what_is_code} entered successfully.")
except Exception as e:
    print(f"Error finding or interacting with CAPTCHA input element: {e}")
    driver.quit()

# Click on the checkbox using JavaScript
try:
    driver.execute_script("""
    var checkbox = document.querySelector("#cbAproveTerm");
    if (checkbox) { 
        checkbox.click(); 
        console.log("Checkbox clicked. Checked status:", checkbox.checked); 
    } else { 
        console.log("Checkbox not found."); 
    }
    """)
    print("Checkbox click simulated.")
except Exception as e:
    print(f"Error simulating click on checkbox: {e}")

# Clicking on the צפייה בתיקי ביטוח button
try:
    button = driver.find_element(By.ID, "butIdent")
    button.click()
    print("Button clicked.")
except Exception as e:
    print("Button not found.", str(e))

# All insurances enteres כל הביטוחים צפייה
div_element = driver.find_element(By.ID, 'butInsuranceOf')

# Check if the element exists
if div_element:
    div_element.click()  # Simulate a click event on the element
    print("Element clicked successfully.")
else:
    print("Element not found.")

# Wait for 5 seconds if local internet has delays
time.sleep(5)

# Download the Excel file
try:
    link = driver.find_element(By.CSS_SELECTOR, 'a[title="יצוא לאקסל"].butCommand.col-sm-3')
    link.click()
    print("Link clicked successfully.")
except Exception as e:
    print("Link not found.", str(e))

driver.quit()

