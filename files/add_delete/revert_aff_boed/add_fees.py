from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time, csv, json

# Constants
TEST_ENVIRONMENT = False
FILE_NAME = "add_fees.csv"
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

# ---------------- EDIT AS NEEDED ----------------
# fee names and fee amounts should coordinate with each other 
fee_names = ["Affiliated/BOED [Jan. 2025]"]

fee_amounts_minor = [0.00]
fee_amounts_school = [0.00]
# --------------------------------------------------

while True:
	user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()

	if user_input == "exit":
		break

	# User defined-range for facility indices
	start_idx = int(input("Enter the START value: "))
	end_idx = int(input("Enter the END value: "))

	curr_idx = start_idx

	# fetch the list of facilities to be referenced later (avoiding back-navigating)
	facility_links = driver.find_elements("xpath", "//a[contains(@class, 'recordDetailIcon')]")
	facility_urls = [link.get_attribute("href") for link in facility_links]

	with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
		# for populating csv file
		writer = csv.writer(file)
		writer.writerow(["Facility Name", "Fee", "Price", "Action"])

		for curr_idx, url in enumerate(facility_urls[start_idx:end_idx+1], start = start_idx):

			# attempt click facility
			try:
				driver.get(url) # open next facility directly in same tab
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "box-tab-caption-active")))
			except:
				print(f"Skipping facility index {curr_idx} due to error:")
				continue
			
			print()
			print(f"Processing current facility index: {curr_idx}")
			curr_facility = driver.find_element("class name", "box-tab-caption-active").text

			# get facility type
			facility_type_element = driver.find_elements(By.XPATH, "//div[contains(@id, 'fld_Readonly')]")[1]  
			facility_type = facility_type_element.text

			# enter facility edit mode
			edit_button = driver.find_element(By.ID, "editObject")
			click_js(driver, edit_button)

			time.sleep(1)

			# Fetch and parse fee data from JSON
			fee_data_elem = driver.find_element("id","fld_servicedurations")
			fee_data = json.loads(fee_data_elem.get_attribute("value"))

			# fetch existing inputs
			fee_inputs = driver.find_elements(By.CSS_SELECTOR, "td.field.noneselected.readmode input.k-formatted-value[placeholder='Fee'][type='text']")

			# Iterate over preexisting fees
			for fee_idx in range(len(fee_names)):
				fee_name = fee_names[fee_idx]

				# Note, the else case only covers Minor and Mini fields, ensure that selected view only has FieldType = School, Mini, Minor ---> Edit as needed
				new_price = str(fee_amounts_school[fee_idx]) if "School" in facility_type else str(fee_amounts_minor[fee_idx])

				# Get the index of the existing fee in fee_data if it exists, otherwise, return -1
				existing_fee_index = next((i for i, fee in enumerate(fee_data) if fee["PriceTypeName"] == fee_name), -1)

				if existing_fee_index != -1:
					print(f"Fee found at index: {existing_fee_index}")
				else:
					print("Fee not found, returning -1")

				# If fee is found, update preexisting fee
				if existing_fee_index != -1:
					
					amount_box = fee_inputs[existing_fee_index]
					amount_box.click()
					action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
					action.send_keys(new_price)

					# trigger update
					action.move_to_element(driver.find_element(By.TAG_NAME, "body")).click().perform()

					# write to csv
					writer.writerow([curr_facility, fee_name, new_price, "Updated"])

					print(f"Updated '{new_price}' price to {fee_name}")
				
				# If fee does not exist, add new fee
				else:
					# enter add fee mode
					add_fee = driver.find_element(By.CSS_SELECTOR, "span[data-field='addserviceduration']")
					click_js(driver, add_fee)

					# search and add fee name
					last_item = driver.find_element(By.CSS_SELECTOR, "#servicedurationselectorwrapper ul li:last-child")
					text_box = last_item.find_element(By.CSS_SELECTOR, "input[placeholder='Search by Name...']")
					text_box.send_keys(fee_name)
					time.sleep(1) # wait for search results to load
					text_box.send_keys(Keys.RETURN)

					# enter fee amount
					amount_box = last_item.find_element(By.CSS_SELECTOR, "span[class='k-widget k-numerictextbox field-web-control']")
					amount_box.click()
					action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
					action.send_keys(new_price)

					# trigger update
					action.move_to_element(driver.find_element(By.TAG_NAME, "body")).click().perform()

					# add to csv
					writer.writerow([curr_facility, fee_name, new_price, "Added"])

					print(f"Added '{new_price}' price to {fee_name}")

					# Wait for UI processing
					time.sleep(2)
			
			# save changes
			save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submitLinkVisible")))

			time.sleep(1)

			click_js(driver, save_button)

			# increment to next facility index
			curr_idx += 1
									   

# finish and close driver window
print("Done!")
driver.close()
