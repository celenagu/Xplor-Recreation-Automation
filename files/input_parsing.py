import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time, csv, json

#constants
read_file_name = "Service-Drop-Ins.csv"

#reading the file
file = pd.read_csv(read_file_name)

#getting the names from the specified column
column_name = "Name"          
names = file[column_name].dropna().tolist()  

# for current_name in names:
#     print(current_name)


# Constants
TEST_ENVIRONMENT = True
FILE_NAME = "updating_timeline.csv"
# login based on the environment
if not TEST_ENVIRONMENT:
	LOGIN_URL = "https://cityofbrampton.perfectmind.com/Menu/MemberRegistration/MemberSignIn"
	USERNAME = "[YOUR LOGIN USERNAME]" # replace
	print("!===WARNING: LIVE MODE===!")
else:
	LOGIN_URL = "https://cityofbramptontest.perfectmind.com/Contacts/MemberRegistration/MemberSignIn"
	USERNAME = "Train8"
	print("===TEST MODE===")

# Webdriver Initialization
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# Functions
def log_save(file, s):
	# writes string to file and prints to console
	file.write(s + "\n") # reformat as needed
	print(s)

def click_js(driver, elem):
	# click element using JavaScript
	driver.execute_script("arguments[0].click();", elem)

# Open website and login
driver.get(LOGIN_URL)
driver.find_element("id", "textBoxUsername").send_keys(USERNAME)
action = ActionChains(driver)


#----------------------------------------------------------------------------------------------------------
while True:
    user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()

    if user_input == "exit":
        break

#-----------------------------finding the 'Section'--------------------------------------------
    service_section = driver.find_element(By.XPATH, "//*[@id='mCSB_2_container']/div[3]/div[3]/div[10]")

    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView();", service_section)
    time.sleep(1)  # Small delay to let the browser adjust

    # Click using JavaScript (if needed)
    driver.execute_script("arguments[0].click();", service_section)

    # Wait for the drop-down options to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='mCSB_2_container']/div[3]/div[3]/div[10]"))
    )

    # Enter the current name
    current_name = "Drop-In Animals"

    # Fix: Use CSS selector instead of CLASS_NAME for multiple classes
    search_input = driver.find_element(By.CSS_SELECTOR, ".search-area.focused")
    search_input.click()  # Click to activate it
    search_input.send_keys(current_name)

    time.sleep(2)  # Ideally use WebDriverWait

    # Dynamically find the correct option that matches current_name
    option_xpath = f"//*[@id='mCSB_2_container']//div[contains(text(), '{current_name}')]"
    option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))

    # Click on the matching option
    option.click()

    # Locate and click the "Done" button
    done_button = driver.find_element(By.CLASS_NAME, "done-btn")  # Check if this is correct
    done_button.click()