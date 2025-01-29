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


#---------------------------------OVERALL LOOP------------------------------------------------
while True:
    user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()

    if user_input == "exit":
        break

#-----------------------------Finding the 'Section'--------------------------------------------
    #Locating the button
    service_section_button = driver.find_element("xpath", "//div[contains(@class, 'search-service-filter filter-custom-section-with-popup')]//div[contains(@class, 'filter-pick-list')]")

    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView();", service_section_button)
    time.sleep(1)  # Small delay to let the browser adjust

    service_section_button.click()

    # Wait for the drop-down options to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-service-filter filter-custom-section-with-popup')]//div[contains(@class, 'filter-pick-list')]"))
    )

#-----------------------------Typing into the search bar------------------------------------------
    # Enter the current name
    current_name = "Drop-In Animals"
	
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'search-service-filter filter-custom-section-with-popup')]//div[contains(@class, 'filter-selectable-options-list')]//div[contains(@class, 'search-area focused')]//input[contains(@class, 'serch-text')]")
        )
    )

    search_input.click()  # Click to activate it
    search_input.send_keys(current_name)

    time.sleep(1) 
#---------------------------Selecting the right checkbox----------------------------------------

    # Needed to create a list and always select the 2nd checkbox as that would be the checkbox associated with current_name
    list_items = driver.find_elements("xpath", "//div[contains(@class, 'search-service-filter filter-custom-section-with-popup')]//div[contains(@class, 'multi-select-filter-template')]//div[contains(@class, 'filter-selectable-options-list')]//div[contains(@class, 'possible-options mCustomScrollbar _mCS_3 mCS-autoHide')]//div[@id='mCSB_3']//div[@id='mCSB_3_container']//ul[@data-bind='foreach: allItemsToShow']")                                                      
    
    # Ensure there are at least 2 items before accessing the second one
    if len(list_items) >= 2:
        second_li = list_items[1]

        # Locate the checkbox inside the second <li>
        second_checkbox_label = second_li.find_element("xpath", ".//label[contains(@class, 'filters-checkbox')]")
        
        # Click the checkbox
        second_checkbox_label.click()
    else:
        print("Less than 2 checkboxes found!")

#-------------------------------Clicking on'Done'-----------------------------------------------
    # Locate and click the "Done" button
    done_button = driver.find_element("xpath", "//div[contains(@class, 'search-service-filter filter-custom-section-with-popup')]//div[contains(@class, 'filter-selectable-options-list')]//div[contains(@class, 'done-btn-wrapper')]//div[contains(@class, 'done-btn')]")
    done_button.click()