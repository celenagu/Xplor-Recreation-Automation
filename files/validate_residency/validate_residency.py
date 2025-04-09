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
# Note: This loop is only to process a single display page in XPLOR (max 1000 items)
# To process views with more than 1000 items, the program will have to be monitored every 1000 items (to manually navigate to next page)
# (May change later)

while True:
	user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()
 
	if user_input == "exit":
		break
	  
	# User defined-range for facility indices
	start_idx = int(input("Enter the START value: "))
	end_idx = int(input("Enter the END value: "))

	curr_idx = start_idx
	  
	# fetch the list of accounts to be referenced later (avoiding back-navigating)
	account_links = driver.find_elements("xpath", "//a[contains(@class, 'recordDetailIcon')]")
	account_urls = [link.get_attribute("href") for link in account_links]
 
	with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
		# for populating csv file
		writer = csv.writer(file)
		writer.writerow(["Client Name", "Account Name", "Account Type", "Account Category", "Account ID", "Client Contact ID", "Validated?"])
			
		# Open up new window
		source_window = driver.current_window_handle
		driver.execute_script("window.open('');")

		all_windows = driver.window_handles
		driver.switch_to.window(all_windows[-1])
		
		for curr_idx, url in enumerate(account_urls[start_idx:end_idx+1], start = start_idx):
			print()
			print(f"Processing current facility index: {curr_idx}")

			account_data = {
				"Account Name": "",         
				"Account Type": "",
				"Account Category": "",
				"Account ID": ""
			}

			client_data = {
				"First Name": "",
				"Last Name": "",
				"Client ID": ""
			}

			# Attempt click account
			try: 
				driver.get(url)	# open next account in new tab
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "box-tab-caption-active")))

				# fetch data needed to populate CSV log (account data)
				account_data["Account Name"] = driver.find_element(By.XPATH, "//tr[contains(@class, 'Name-wrapper')]//div[contains(@class, 'field-web-control')]").text
				account_data["Account Type"] = driver.find_element(By.XPATH, "//tr[contains(@class, 'AccountType-wrapper')]//div[contains(@class, 'field-web-control')]").text
				account_data["Account Category"] = driver.find_element(By.XPATH, "//tr[contains(@class, 'AccountCategory-wrapper')]//div[contains(@class, 'field-web-control')]").text
				account_data["Account ID"] = driver.find_element(By.XPATH, "//tr[contains(@class, 'RecordName-wrapper')]//div[contains(@class, 'field-web-control')]").text
				
				# get clients associated with account
				clients = driver.find_elements("xpath", "//li[contains(@class, 'family-member') and not (@id='family-member-template')]//h3[contains(@class, 'family-member-name')]")


				for client in clients:
					click_js(driver, client)
					WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "box-tab-caption-active")))

					input("Paused. Press Enter to continue...")

					# Fetch client data
					client_data["First Name"] = driver.find_element(By.XPATH, "//tr[contains(@class, 'FirstName-wrapper')]//div[contains(@class, 'field-web-control')]").text
					client_data["Last Name"] = driver.find_element(By.XPATH, "//tr[contains(@class, 'LastName-wrapper')]//div[contains(@class, 'field-web-control')]").text
					client_data["Client ID"] = driver.find_element(By.XPATH, "//tr[contains(@class, 'RecordName-wrapper')]//div[contains(@class, 'field-web-control')]").text

					# Handle updating residency

					# Populate CSV file

					# Navigate back to accounts
					back = driver.find_element(By.XPATH, "//a[contains(@class, 'back-button-link')]")
					click_js(driver, back)

			except Exception as e:
				print(f"Failed to update account index {curr_idx} due to error:\n{e}")
