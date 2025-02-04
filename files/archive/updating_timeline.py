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

def process_page(driver, event_data, edit_buttons):
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
		repeat_tab = WebDriverWait(driver, 15).until(
			EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'edit-event-header')]//li[@id='editEventTabs-tab-2']"))
		)

		# repeat_tab.click()
		click_js(driver, repeat_tab)

		# Dismiss overlay alerts blocking view
		while True:
			overlay_notif = driver.find_elements("xpath", "//div[contains(@class, 'k-animation-container')]//div[contains(@class, alert)]")

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

		# ---------- In booking tab ---------------------

		booking_tab = WebDriverWait(driver, 15).until(
			EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'edit-event-header')]//li[@id='editEventTabs-tab-3']"))
		)

		booking_tab.click()

		# ---------- Update booking times ----------------

		# Updating registration times
		settings = []
		settings.append(driver.find_element(By.XPATH, "//a[contains(@class, 'admin-advanced-settings')]"))
		settings.append(driver.find_element(By.XPATH, "//a[@class='advanced-settings']"))

		for settings_btn in settings:

			click_js(driver, settings_btn)

			chg_buttons = driver.find_elements("xpath", "//div[@id= 'registrationDatesAdvancedSettings']//span[contains(@class, 'change-date-btn')]")

			for i in range(0, 3):
				click_js(driver, chg_buttons[i])

				hours_btn = driver.find_element(By.XPATH, "//div[@id='registrationDateOptionsSelector']//div[contains(@class, 'reg-date-options-selector-row')]//span[contains(text(), '# Hours')]")
				click_js(driver, hours_btn)
				
				if i != 0:
					inc_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'reg-date-selector')]//span[contains(@class, 'k-link-increase')]")
					
					for j in range(24):
						inc_btn.click()

				done = driver.find_element(By.XPATH, "//div[@id='registrationDateOptionsSelector']//button[contains(@class, 'reg-date-done-btn')]")
				click_js(driver, done)

			# save registration times
			save = driver.find_element(By.XPATH, "//a[@title='Save' and contains(@class, 'pm-confirm-button')]")
			click_js(driver, save)

		print("Registration times updated.")

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



new_date = "2025-03-23"

while True:
	print("")
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
		writer.writerow(["Event"])

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

		original_tab = driver.current_window_handle

		# if the current service has no events, skip
		if len(event_data) == 0:
			print("No events, skip")
			continue
		
		# if the current service exceeds 100 events, do extra processing
		elif len(event_data) == 100:
			try:
				limit = driver.find_element(By.XPATH, "//span[contains(@class, 'events-limit-exceeded-text-bold')]")
				if limit:
					print("Events limit exceeded")
					continue
			except Exception:
				pass

		# otherwise (0, 100] events, process as normal
		process_page(driver, event_data, edit_buttons)


# finish and close driver window
print("Done!")
driver.close()
