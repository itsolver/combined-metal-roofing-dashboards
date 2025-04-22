"""
This script is used to open a Chrome browser window on the second monitor.
"""
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# Set up a logger
logger = logging.getLogger('monitor2')

# Set the log level
logger.setLevel(logging.INFO)

# Create a rotating file handler that logs even debug messages
handler = RotatingFileHandler('monitor2.log', maxBytes=20000, backupCount=5)
handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--app=https://swroofing.sharepoint.com/:x:/g/Edj-N_p-SY9Hs0gk1aQkaE0BhsBm0DKXYZqfhDx9Yc_-_g?e=u99p7B&nav=MTVfezA5MzgzQkQ5LUNDQUYtNEVGMS05NzFDLUY0NUJEQjI2MkMzOX0')
chrome_options.add_argument('--user-data-dir=C:\\monitor2')
#chrome_options.add_argument('--window-position=0,0') # Set window position for monitor 1
chrome_options.add_argument('--window-position=3840,0') # Set window position for monitor 2
chrome_options.add_argument('--kiosk') # disable kiosk while troubleshooting
#chrome_options.add_argument('--window-size=3840,2160') # Set window size
# Hide "Chrome is being controlled by automated test software" notification
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--no-first-run')

logging.debug('Chrome options set.')

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
try:
    logging.info('Trying to load page...')
    WebDriverWait(driver, 60).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    logging.info("Live Project Status Page loaded successfully")

    # # Switch to the first frame on the page
    # logging.debug('Trying to switch to the first frame...')
    # wait = WebDriverWait(driver, 60)  # wait up to 60 seconds
    # frame = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    # driver.switch_to.frame(frame)

    # # Force Ribbon to hide by clicking Always Show then Automatically Hide
    # logging.debug('Trying to find RibbonModeToggle...')
    # ribbon_model_toggle = wait.until(EC.presence_of_element_located((By.ID, 'RibbonModelToggle')))

    # # click on the element
    # logging.debug('Trying to click on RibbonModeToggle...')
    # ribbon_model_toggle.click()

    # logging.debug('Trying to find Show Menu...')
    # showmenu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#MultilineRibbon-RibbonModeToggleDropdown > div > ul > li:nth-child(3) > div > ul > li:nth-child(2) > button > div > span")))


    # logging.debug('Trying to click on Show Menu...')
    # showmenu.click()

    # logging.debug('Trying to click on RibbonModeToggle again...')
    # ribbon_model_toggle.click()

    # logging.debug('Trying to find Hide Menu...')
    # hidemenu =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#MultilineRibbon-RibbonModeToggleDropdown > div > ul > li:nth-child(3) > div > ul > li:nth-child(3) > button > div > span")))

    # logging.debug('Trying to click on Hide Menu...')
    # hidemenu.click()

    # Keep the browser open
    while True:
        time.sleep(600)
        driver.refresh()
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    logging.info("Keyboard interrupt detected. Terminating the script...")

    # Clean up and exit
    driver.quit()   # Quit the ChromeDriver instance
    sys.exit(0)
except WebDriverException as e:
    if isinstance(e, TimeoutException):
        logging.error("A TimeoutException occurred: %s", str(e), exc_info=True)
    else:
        logging.error("A WebDriverException occurred: %s", str(e), exc_info=True)
    driver.quit()   # Quit the ChromeDriver instance
    sys.exit(1)
