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
 
#constants
read_file_name = "barcodes-csv.csv"
 
#reading the file
file_names = pd.read_csv(read_file_name)
 
#getting the barcodes from the specified column
column_name = "EventID"          
all_barcodes = file_names[column_name].dropna().tolist()  
 
 
# Constants
TEST_ENVIRONMENT = True
FILE_NAME = "updating_registration.csv"
new_date = "2025-03-23"
 
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
 
# ----------------------------------- FUNCTIONS ------------------------------------------------------------------------
def log_save(file, s):
    # writes string to file and prints to console
    file.write(s + "\n") # reformat as needed
    print(s)
 
def click_js(driver, elem):
    # click element using JavaScript
    driver.execute_script("arguments[0].click();", elem)
 
def wait_for_page_load(driver):
    # waits for page to finish updating
    try:
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script(
                "return window.performance.getEntriesByType('resource').every(r => r.responseEnd > 0);"
            )
        )
        print("Network requests completed.")
    except TimeoutException:
        print("Warning: Network idle check timed out.")
 
def process_page(driver, event_data, edit_buttons, original_tab, new_date):
    # looping through each program on the page, for each event:
    for idx in range(0, len(event_data)):
        event_name = event_data[idx].get_attribute("textContent")
        print("")
        print(f"Processing index: {idx}")
        print(event_name)
        writer.writerow([event_name])
 
        # click edit and focus on new tab
        click_js(driver, edit_buttons[idx])
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
 
   
        # -------------------------- IN EDIT PANEL -------------------------
 
        # ------------ In repeat tab --------------------
        repeat_tab = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'edit-event-header')]//li[@id='editEventTabs-tab-2']"))
        )
 
        # repeat_tab.click()
        click_js(driver, repeat_tab)
 
        # Dismiss overlay alerts blocking view
        while True:
            overlay_notif = driver.find_elements(By.XPATH, "//div[contains(@class, 'k-animation-container')]//div[contains(@class, alert)]")
 
            if not overlay_notif:
                break
 
            for overlay in overlay_notif:
                try:
                    click_js(driver, overlay)
                except Exception:
                    pass
 
 
        # ----------- update date ---------------------
 
        date = driver.find_element(By.XPATH, "//input[contains(@class, 'k-recur-until')]")
        date.click()
        action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
        driver.execute_script("arguments[0].value = arguments[1];", date, new_date)
        date.send_keys(Keys.ENTER)
       
        # trigger update
        action.move_to_element(driver.find_element(By.TAG_NAME, "body")).click().perform()
        print("Date updated.")
 
        # ---------- Save all changes-------------------------
        save_final = driver.find_elements(By.XPATH, "//div[contains(@class, 'k-edit-form-container')]//span[contains(@class, 'k-button-text')]")
        click_js(driver, save_final[1])
 
        # wait for page to load
        wait_for_page_load(driver)
 
        try:
            # click proceed
            proceed = driver.find_element(By.XPATH, "//a[contains(@class, 'cm-button') and @title='Proceed Anyway']")
            click_js(driver, proceed)
            wait_for_page_load(driver)
        except Exception:
            pass
 
        print("Saved.")
 
        driver.close()
        driver.switch_to.window(original_tab)
 


# -----------------------------------------------------------------------------------------------------------------------------------
 
# Open website and login
driver.get(LOGIN_URL)
driver.find_element("id", "textBoxUsername").send_keys(USERNAME)
action = ActionChains(driver)
 
 
#---------------------------------OVERALL LOOP------------------------------------------------
while True:
    user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()
 
    if user_input == "exit":
        break
 
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        # for populating csv file
        writer = csv.writer(file)
        writer.writerow(["Event"])
#-----------------------------Looping through csv file------------------------------------------
        for barcode in all_barcodes:
            print(barcode)
       
#-----------------------------Search by barcode--------------------------------------------
            #Locating the button
            keyword_button = driver.find_element("xpath", "//div[contains(@class, 'k-content')]//div[contains(@class, 'pm-search-wrapper search-input-container')]//input[@type='text']")
 
            click_js(driver, keyword_button)
            print("found it")
 
            #keyword_button.click()  # Click to activate it
            modified_barcode = "00" + str(barcode)
            keyword_button.clear()
            # action.key_down(Keys.CONTROL).key_down('a').perform()
            keyword_button.send_keys(modified_barcode)
            time.sleep(1)
            keyword_button.send_keys(Keys.ENTER)
            time.sleep(1)
 
 #----------------------------------Update program times-----------------------------------------------
 
            #For now a temporary question
            temp_question = input("Press ENTER to confirm that fees and timelines have been adjusted for this Service: ").strip().lower()
 
            # check to see if current service has events, if none, skip
            driver.implicitly_wait(0)
            check_present = driver.find_elements(By.XPATH, "//td[@colspan='23']")
            if check_present:
                print("No events, skip")
                driver.implicitly_wait(10)
                continue
            driver.implicitly_wait(10)
           
            # Extract currently visible events
            event_data = driver.find_elements(By.XPATH, "//div[contains(@class, 'grid-panel')]//div[contains(@class, 'activity-name')]")
 
            # Extract edit buttons
            edit_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'grid-panel')]//span[contains(@class, 'edit-text') and contains(@class, 'edit-event')]")
 
            # print(f"Number of programs: {len(event_data)}")
 
            original_tab = driver.current_window_handle
           
            # if the current service exceeds 100 events, do extra processing
            if len(event_data) == 100:
                try:
                    limit = driver.find_element(By.XPATH, "//span[contains(@class, 'events-limit-exceeded-text-bold')]")
                    if limit:
                        print("Events limit exceeded")
                        continue
                except Exception as e:
                    print(f"Exception occured: {str(e)}")
 
            # otherwise (0, 100] events, process as normal
            process_page(driver, event_data, edit_buttons, original_tab, new_date)
           
            time.sleep(2)
           
 
 