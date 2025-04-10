import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, csv, json



# Constants
TEST_ENVIRONMENT = True
FILE_NAME = "update_log.csv"
new_date = "2060-01-1"
 
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
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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



while True:
    user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()
 
    if user_input == "exit":
        break

    #after clicking on the client...

    #find the edit button
    edit_button = driver.find_element(By.ID, "editObject")
    click_js(driver, edit_button)
    time.sleep(2)

    #ERROR HERE
    #locate where the toggle for the 'Validation' section
    validation_button = driver.find_element("xpath", "//tr[contains(@class, 'AccountValidation-wrapper')]//input[contains(@class, 'xpl-toggle')]")
    print("found it")

    #check to see if its been clicked or not -> its True if its been clicked and False if it hasn't been clicked yet
    status_check = driver.find_element("xpath", "//div[contains(@class, 'Checkbox-wrapper AccountValidation-wrapper')]//i[contains(@class, 'field-web-control')]//i[contains(@class, 'pmFieldDependency')]")
    status = status_check.get_attribute("value") 

    #making an updated version of 'status' that's a boolean
    status_bool = status.lower() == "true"

    #if the status is False, we need to click it...
    if status_bool == False:

        print("Clicking the toggle...")

        click_js(driver, validation_button)

        #find the date button
        date_button = driver.find_element("xpath", "//div[contains(@class, 'Checkbox-wrapper AccountValidation-wrapper')]//i[contains(@class, 'Date-wrapper AccountResidencyValidatedOn-wrapper')]//i[contains(@class, 'pmdatepicker hasDatepicker k-valid')]")
        date_button.clear()
        date_button.send_keys(new_date)
        time.sleep(1)

        #find the save button
        save = driver.find_element(By.XPATH, "//a[@title='Save' and contains(@class, 'pm-confirm-button xpl-button submitLinkVisible')]")
        click_js(driver, save)
        time.sleep(4)

        print("Saved")

