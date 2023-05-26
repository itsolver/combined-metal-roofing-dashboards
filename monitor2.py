import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--kiosk')
#chrome_options.add_argument('--app=https://swroofing.sharepoint.com/:x:/r/Operations/Live%20Project%20Status.xlsx?d=we1b6b747158f4d568451c688c3517f83&csf=1&web=1&e=bJkYxd&nav=MTVfezhFNTVCODkzLTcxRkYtNEZEMi1CODZCLURFM0VFMjMyQTY3Mn0')
chrome_options.add_argument('--user-data-dir=C:\\monitor2')
chrome_options.add_argument('--window-position=3840,0') # Set window position

# Hide "Chrome is being controlled by automated test software" notification
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# use new window for debugging
chrome_options.add_argument('--new-window https://swroofing.sharepoint.com/:x:/r/Operations/Live%20Project%20Status.xlsx?d=we1b6b747158f4d568451c688c3517f83&csf=1&web=1&e=bJkYxd&nav=MTVfezhFNTVCODkzLTcxRkYtNEZEMi1CODZCLURFM0VFMjMyQTY3Mn0')

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Keep the browser open
    while True:
        # Wait for the page to load
        WebDriverWait(driver, 60).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("Live Project Status Page loaded successfully")

        # Switch to the first frame on the page
        driver.switch_to.frame(0)

        # Force Ribbon to hide by clicking Always Show then Automatically Hide
        nav = driver.find_element(By.ID, "RibbonModeToggle")
        print("Found RibbonModeToggle")
        # click on the element
        nav.click()
        print("Clicked RibbonModeToggle")

        # Wait for the element to be present on the page
        wait = WebDriverWait(driver, 10)
        showmenu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#MultilineRibbon-RibbonModeToggleDropdown > div > ul > li:nth-child(3) > div > ul > li:nth-child(2) > button > div > span")))
        print("Found Show Menu")
        showmenu.click()
        print("Clicked Show Menu")
        # click on the element
        nav.click()
        print("Clicked RibbonModeToggle")

        hidemenu = driver.find_element(By.CSS_SELECTOR, "#MultilineRibbon-RibbonModeToggleDropdown > div > ul > li:nth-child(3) > div > ul > li:nth-child(3) > button > div > span")
        print("Found Hide Menu")
        hidemenu.click()
        print("Clicked Hide Menu")
        time.sleep(30)
        
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    print("Keyboard interrupt detected. Terminating the script...")
    # Clean up and exit
    driver.quit()   # Quit the ChromeDriver instance
    sys.exit(0)
