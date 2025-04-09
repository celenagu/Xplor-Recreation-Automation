import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
 
import time, csv, json

from webdriver_manager.chrome import ChromeDriverManager
 
read_file_name = "barcodes.csv"
 
#reading the file
file_names = pd.read_csv(read_file_name, dtype={"EventID": str})
 
#getting the barcodes from the specified column
column_name = "EventID"          
all_barcodes = file_names[column_name].dropna().tolist()  
 
 
# Constants
TEST_ENVIRONMENT = False
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
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)
 
# ----------------------------------- FUNCTIONS ------------------------------------------------------------------------
def log_save(file, s):
    # writes string to file and prints to console
    file.write(s + "\n") # reformat as needed
    print(s)
 
def click_js(driver, elem):
    # click element using JavaScript
    driver.execute_script("arguments[0].click();", elem)

# -----------------------------------------------------------------------------------------------------------------------------------
 
# Open website and login
driver.get(LOGIN_URL)
# driver.find_element("id", "textBoxUsername").send_keys(USERNAME)
action = ActionChains(driver)
 
 
#---------------------------------OVERALL LOOP------------------------------------------------
while True:
	user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()
 
	if user_input == "exit":
		break
 
