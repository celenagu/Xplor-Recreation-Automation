from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, csv

# Constants
TEST_ENVIRONMENT = True
FILE_NAME = "locations.csv"

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


	with open(FILE_NAME,"w", newline="", encoding="utf-8") as file:
		# for populating csv file
		writer = csv.writer(file)
		writer.writerow(["Location"])	# CSV header

		locations = driver.find_elements("xpath", "//li[contains(@class, 'k-item') and contains(@class, 'location')]//span[contains(@class, 'k-in')]")
		for location in locations:
			print(location.get_attribute("title"))
			writer.writerow([location.get_attribute("title")])
			

# finish and close driver window
print("Done!")
driver.close()
