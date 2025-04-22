import time
import sys
import logging
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager, ChromeType

# Set up logging for monitor1-window1.py and monitor1-window2.py
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('monitor1.log', maxBytes=20000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
# Use new window for development
#chrome_options.add_argument('--new-window https://app.connecteam.com/index.html#/index/shift-scheduler/shiftscheduler/1238353')
chrome_options.add_argument('--app=https://app.connecteam.com/index.html#/index/shift-scheduler/shiftscheduler/1238353')
chrome_options.add_argument('--user-data-dir=C:\\monitor1')
chrome_options.add_argument('--window-position=0,0') # Set window position
chrome_options.add_argument('--window-size=1920,2160') # Set window size
# Hide "Chrome is being controlled by automated test software" notification
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--no-first-run')

# Function to download ChromeDriver with retries
def get_chromedriver_with_retries(max_attempts=3, delay=5):
    attempt = 1
    while attempt <= max_attempts:
        try:
            logger.info(f"Attempt {attempt} to download ChromeDriver...")
            driver_path = ChromeDriverManager().install()
            logger.info("ChromeDriver downloaded successfully.")
            return driver_path
        except Exception as e:
            logger.error(f"Failed to download ChromeDriver on attempt {attempt}: {str(e)}")
            if attempt == max_attempts:
                logger.error("Max attempts reached. Exiting...")
                raise
            time.sleep(delay)
            attempt += 1

# Set up the driver with retry logic
try:
    driver_path = get_chromedriver_with_retries()
    driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
except Exception as e:
    logger.error(f"Failed to initialize ChromeDriver: {str(e)}")
    sys.exit(1)

# Main script
try:
    # Sign in to Connecteam if not already signed in
    # Wait for the page to load
    WebDriverWait(driver, 60).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    print("Connect Team Page loaded successfully")
    # Detect if sign in is required (https://app.connecteam.com/index.html#/Login)
    if driver.current_url == 'https://app.connecteam.com/index.html#/Login':
        print("Sign in required.")
        # Enter mobile number
        mobile_number = '415559155 ' # Replace with actual mobile number
        mobile_number_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ct-phone-input-control')))
        mobile_number_input.send_keys(mobile_number)
        print("Blair's Mobile number entered")
        # Hit enter
        mobile_number_input.send_keys(Keys.ENTER)
        print("Enter key pressed")
        # Keep the browser open
    while True:
        time.sleep(300)
        driver.refresh() # Refresh the Chrome window
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    print("Keyboard interrupt detected. Terminating the script...")
    # Clean up and exit
    driver.quit()   # Quit the ChromeDriver instance
    sys.exit(0)
