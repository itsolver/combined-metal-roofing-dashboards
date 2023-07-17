import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Setup logging configuration
logging.basicConfig(filename='monitor2.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--app=https://swroofing.sharepoint.com/:x:/g/Edj-N_p-SY9Hs0gk1aQkaE0BhsBm0DKXYZqfhDx9Yc_-_g?e=u99p7B&nav=MTVfezA5MzgzQkQ5LUNDQUYtNEVGMS05NzFDLUY0NUJEQjI2MkMzOX0')
chrome_options.add_argument('--user-data-dir=C:\\monitor2')
chrome_options.add_argument('--window-position=0,0') # Set window position for monitor 1
# chrome_options.add_argument('--window-position=3840,0') # Set window position for monitor 2
# chrome_options.add_argument('--kiosk') # disable kiosk while troubleshooting
chrome_options.add_argument('--window-size=3840,2160') # Set window size
# Hide "Chrome is being controlled by automated test software" notification
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

logging.debug('Chrome options set.')

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    logging.info('Trying to load page...')
    WebDriverWait(driver, 60).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    logging.info("Live Project Status Page loaded successfully")

    wait = WebDriverWait(driver, 10)  # wait up to 10 seconds

    # Pause script until a key is pressed
    input("Press any key to continue...")

    # Switch to the first frame on the page
    logging.debug('Trying to switch to the first frame...')
    wait = WebDriverWait(driver, 10)  # wait up to 10 seconds
    frame = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))

    driver.switch_to.frame(frame)

    # Force Ribbon to hide by clicking Always Show then Automatically Hide
    logging.debug('Trying to find RibbonModeToggle...')
    nav = driver.find_element(By.ID, "RibbonModeToggle")

    # click on the element
    logging.debug('Trying to click on RibbonModeToggle...')
    nav.click()

    logging.debug('Trying to find Show Menu...')
    showmenu = driver.find_element(By.CSS_SELECTOR, "#MultilineRibbon-RibbonModeToggleDropdown > div > ul > li:nth-child(3) > div > ul > li:nth-child(2) > button > div > span")

    logging.debug('Trying to click on Show Menu...')
    showmenu.click()

    logging.debug('Trying to click on RibbonModeToggle again...')
    nav.click()

    logging.debug('Trying to find Hide Menu...')
    hidemenu = driver.find_element(By.CSS_SELECTOR, "#MultilineRibbon-RibbonModeToggleDropdown > div > ul > li:nth-child(3) > div > ul > li:nth-child(3) > button > div > span")

    logging.debug('Trying to click on Hide Menu...')
    hidemenu.click()

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
except Exception as e:
    logging.error(f"An error occurred: {str(e)}", exc_info=True)
    driver.quit()   # Quit the ChromeDriver instance
    sys.exit(1)
