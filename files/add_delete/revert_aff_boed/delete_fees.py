from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, csv

# Constants
TEST_ENVIRONMENT = True
FILE_NAME = "delete_fees.csv"

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
	file.write(s + ",") # reformat as needed
	print(s)

def click_js(driver, elem):
	# click element using JavaScript
	driver.execute_script("arguments[0].click();", elem)

# Open website and login
driver.get(LOGIN_URL)
driver.find_element("id", "textBoxUsername").send_keys(USERNAME)


while True:
	user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()

	if user_input == "exit":
		break

	# User defined-range for facility indices
	start_idx = int(input("Enter the START value: "))
	end_idx = int(input("Enter the END value: "))

	curr_idx = start_idx

	# fetch the list of facilities to be referenced later
	facility_links = driver.find_elements("xpath", "//a[contains(@class, 'recordDetailIcon')]")

	facility_urls = [link.get_attribute("href") for link in facility_links]


	with open(FILE_NAME,"w", newline="", encoding="utf-8") as file:
		# for populating csv file
		writer = csv.writer(file)
		writer.writerow(["Facility Name", "Fee Name", "Deleted?"])	# CSV header

		for curr_idx, url in enumerate(facility_urls[start_idx:end_idx + 1], start = start_idx):

			# attempt click on facility with retries
			try:
				driver.get(url) # open next facility directly in same tab
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "box-tab-caption-active")))

			except:
				print(f"Skipping facility index {curr_idx} due to error.")
				continue

			print(f"Processing current facility index: {curr_idx}")
			curr_facility = driver.find_element("class name", "box-tab-caption-active").text

			# enter facility edit mode
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "editObject"))).click()

			# fetch and parse fee data from JSON
			fee_data_elem = driver.find_element("id","fld_servicedurations")
			fee_data = json.loads(fee_data_elem.get_attribute("value"))
			delete_buttons = driver.find_elements("xpath", "//div[contains(@class, 'field-control-wrapper add-multiple-fee')]//i[contains(@class, 'pm-plain-button')]")


			# iterate over fees ----> ISSUE: LISTS START AT INDEX 0
			for fee_idx in range(0, len(fee_data)):
				fee_name = fee_data[fee_idx].get("PriceTypeName")
				is_deleted = "Yes" if "Affiliated/BOED [Jan. 2025]" in fee_name else "No"

				# write data to CSV
				writer.writerow([curr_facility, fee_name, is_deleted])

				if is_deleted == "Yes":
					click_js(driver, delete_buttons[fee_idx])


			# save changes
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submitLinkVisible"))).click()

			time.sleep(1)

# finish and close driver window
print("Done!")
driver.close()
