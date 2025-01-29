from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, csv, json

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

# Obtain all services from txt file


services = []
exceed = []
new_date = "2025-03-23"

while True:
	user_input = input("Press ENTER to start/continue or type 'exit' to end: ").strip().lower()

	if user_input == "exit":
		break

	# # User defined-range for indices
	# start_idx = int(input("Enter the START value: "))
	# end_idx = int(input("Enter the END value: "))

	# curr_idx = start_idx

	with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
		# for populating csv file
		writer = csv.writer(file)
		writer.writerow(["Event", "Location", "Price", "Action"])

		# ------------ Code to iterate over all services -------------
		# for service in services:
		# --------------------------------------------------------------

		# print(f"Processing service: {service}")

		# ---- Code to click service, load page, check to see if number on page exceeds limit


		# Extract currently visible events
		event_data = driver.find_elements("xpath", "//div[contains(@class, 'grid-panel')]//div[contains(@class, 'activity-name')]")

		# Extract edit buttons
		edit_buttons = driver.find_elements("xpath", "//div[contains(@class, 'grid-panel')]//span[contains(@class, 'edit-text') and contains(@class, 'edit-event')]")

		print(f"Number of programs: {len(event_data)}")
		print(f"Number of edit buttons: {len(edit_buttons)}")

		# -- click edit button, open in new tab

		original_tab = driver.current_window_handle
		click_js(driver, edit_buttons[0])

		# focus on newly-opened tab
		windows = driver.window_handles
		driver.switch_to.window(windows[-1])

		time.sleep(8)

		# -------------------------- IN EDIT PANEL -------------------------

		# In repeat tab
		repeat_tab = WebDriverWait(driver, 15).until(
			EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'edit-event-header')]//li[@id='editEventTabs-tab-2']"))
		)

		repeat_tab.click()

		# # Dismiss overlay alerts blocking view
		# overlay_notif = driver.find_elements("xpath", "//div[contains(@class, 'k-animation-container')]//div[contains(@class, alert)]")

		# print(f"number of overlays: {len(overlay_notif)}")
		# if len(overlay_notif) != 0:
		# 	click_js(driver, overlay_notif[len(overlay_notif)-1])

		# update date
		date = driver.find_element(By.XPATH, "//input[contains(@class, 'k-recur-until')]")
		date.click()
		action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
		driver.execute_script("arguments[0].value = arguments[1];", date, new_date)
		date.send_keys(Keys.ENTER)
		
		# trigger update
		action.move_to_element(driver.find_element(By.TAG_NAME, "body")).click().perform()
		print("Date updated.")

		# In booking tab

		booking_tab = WebDriverWait(driver, 15).until(
			EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'edit-event-header')]//li[@id='editEventTabs-tab-3']"))
		)

		booking_tab.click()

		# Update booking times
		admin_settings = driver.find_element(By.XPATH, "//a[contains(@class, 'admin-advanced-settings')]")
		click_js(driver, admin_settings)

		chg_buttons = driver.find_elements("xpath", "//div[@id= 'registrationDatesAdvancedSettings']//span[contains(@class, 'change-date-btn')]")
		click_js(driver, chg_buttons[0])

		hours_btn = driver.find_element(By.XPATH, "//div[@id='registrationDateOptionsSelector']//div[contains(@class, 'reg-date-options-selector-row')]//span[contains(text(), '# Hours')]")
		click_js(driver, hours_btn)

		done = driver.find_element(By.XPATH, "//div[@id='registrationDateOptionsSelector']//button[contains(@class, 'reg-date-done-btn')]")
		click_js(driver, done)



		online_settings = driver.find_element(By.XPATH, "//a[contains(@class, 'advanced-settings')]")



		# Click repeat tab
		# for item in edit_buttons:
		# 	click_js(driver, item)

		# driver.close()
		# driver.switch_to.window(original_tab)

									   

# finish and close driver window
print("Done!")
driver.close()
