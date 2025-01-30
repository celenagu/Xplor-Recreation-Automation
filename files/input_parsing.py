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


#---------------------------------OVERALL LOOP------------------------------------------------
while True:
    user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()

    if user_input == "exit":
        break

#-----------------------------Looping through csv file------------------------------------------
    for current_names in names:
		
#-----------------------------Finding the 'Section'--------------------------------------------
        #Locating the button
        service_section_button = driver.find_element("xpath", "//div[contains(@class, 'search-service-filter filter-custom-section-with-popup')]//div[contains(@class, 'filter-pick-list')]")

        click_js(driver, service_section_button)

        # Wait for the drop-down options to load
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-service-filter filter-custom-section-with-popup')]//div[contains(@class, 'filter-pick-list')]"))
        )
		
#-----------------------------Typing into the search bar------------------------------------------
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'search-service-filter filter-custom-section-with-popup')]//div[contains(@class, 'filter-selectable-options-list')]//div[contains(@class, 'search-area focused')]//input[contains(@class, 'serch-text')]")
            )
        )

        search_input.click()  # Click to activate it
        search_input.send_keys(current_names)

        time.sleep(1) 
#---------------------------Selecting the right checkbox----------------------------------------

        # Needed to create a list and always select the 2nd checkbox as that would be the checkbox associated with current_name                                                     
        list_items = driver.find_elements("xpath", "//div[contains(@class, 'search-service-filter')]//div[contains(@class, 'filter-selectable-options-list')]//label[contains(@class, 'filters-checkbox')]")
        click_js(driver, list_items[1])
        time.sleep(1)
		
#-------------------------------Clicking on'Done'-----------------------------------------------
        # Locate and click the "Done" button
        done_button = driver.find_element("xpath", "//div[contains(@class, 'search-service-filter')]//div[contains(@class, 'done-btn')]")
        done_button.click()
 #----------------------------------Celena's Code-----------------------------------------------
        #For now a temporary question
        temp_question = input("Press ENTER to confirm that fees and timelines have been adjusted for this Service: ").strip().lower()

 #---------------------------------Clicking Reset-----------------------------------------------
        reset_button  = driver.find_element(By.XPATH, "//div[contains(@class, 'search-service-filter')]//span[contains(@class, 'reset-filter-link')]")
        if reset_button:
            print("Reset button found, clicking now...")
            click_js(driver, reset_button)
        else:
            print("Reset button not found!")

        time.sleep(2)
