from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--kiosk')
# chrome_options.add_argument('--app=https://app.connecteam.com/index.html#/index/shift-scheduler/shiftscheduler/1238353')
chrome_options.add_argument('--user-data-dir=C:\\monitor1')
chrome_options.add_argument('--window-position=-1920,0') # Set window position

# Hide "Chrome is being controlled by automated test software" notification
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# use new window for debugging
chrome_options.add_argument('--new-window https://app.connecteam.com/index.html#/index/shift-scheduler/shiftscheduler/1238353')

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Your automation code goes here...

# Sign in to Connecteam if not already signed in
# Wait for the page to load
WebDriverWait(driver, 60).until(lambda d: d.execute_script('return document.readyState') == 'complete')
print("Page loaded successfully")
# Detect if sign in is required (https://app.connecteam.com/index.html#/Login)
if driver.current_url == 'https://app.connecteam.com/index.html#/Login':
    # Enter mobile number
    mobile_number = '415559155 ' # Replace with actual mobile number
    mobile_number_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'automation-phone-text-box')))
    mobile_number_input.send_keys(mobile_number)
    # Hit enter
    mobile_number_input.send_keys(Keys.ENTER)

# Keep the browser open
while True:
    time.sleep(1)