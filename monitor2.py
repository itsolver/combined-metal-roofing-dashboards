"""
This script is used to open a Chrome browser window on the second monitor.
"""
import sys
import time
import logging
import platform
import os
import stat
import shutil
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager, ChromeType

# Set up logging for monitor2.py
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('monitor2.log', maxBytes=20000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--app=https://swroofing.sharepoint.com/:x:/g/Edj-N_p-SY9Hs0gk1aQkaE0BhsBm0DKXYZqfhDx9Yc_-_g?e=u99p7B&nav=MTVfezA5MzgzQkQ5LUNDQUYtNEVGMS05NzFDLUY0NUJEQjI2MkMzOX0')
chrome_options.add_argument('--user-data-dir=C:\\monitor2')
chrome_options.add_argument('--window-position=3840,0') # Set window position for monitor 2
chrome_options.add_argument('--window-size=1920,2160') # Set window size
# Hide "Chrome is being controlled by automated test software" notification
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--no-first-run')

# Set up the driver
try:
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logger.info("ChromeDriver initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize ChromeDriver: {str(e)}")
    sys.exit(1)

# Main script
try:
    # Wait for the page to load
    WebDriverWait(driver, 60).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    logger.info("Live Project Status Page loaded successfully")

    # Keep the browser open
    while True:
        time.sleep(600)
        driver.refresh()
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    logger.info("Keyboard interrupt detected. Terminating the script...")
    # Clean up and exit
    driver.quit()   # Quit the ChromeDriver instance
    sys.exit(0)
except WebDriverException as e:
    if isinstance(e, TimeoutException):
        logger.error("A TimeoutException occurred: %s", str(e), exc_info=True)
    else:
        logger.error("A WebDriverException occurred: %s", str(e), exc_info=True)
    driver.quit()   # Quit the ChromeDriver instance
    sys.exit(1)
