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

def set_executable_permissions(file_path):
    """Set executable permissions on the ChromeDriver file."""
    try:
        # Make the file executable
        os.chmod(file_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        logger.info(f"Set executable permissions on {file_path}")
    except Exception as e:
        logger.error(f"Failed to set permissions on {file_path}: {str(e)}")
        raise

def cleanup_chromedriver():
    """Clean up any existing ChromeDriver files and processes."""
    try:
        # Kill any existing ChromeDriver processes
        os.system('taskkill /f /im chromedriver.exe')
        time.sleep(1)  # Give it time to terminate
        
        # Clean up ChromeDriver files in common locations
        cleanup_paths = [
            "chromedriver.exe",
            os.path.join(os.getcwd(), "chromedriver.exe"),
            os.path.join(os.path.expanduser("~"), ".wdm", "drivers", "chromedriver")
        ]
        
        for path in cleanup_paths:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    logger.info(f"Removed file: {path}")
                elif os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                    logger.info(f"Removed directory: {path}")
            except Exception as e:
                logger.warning(f"Failed to clean up {path}: {str(e)}")
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")

# Function to download ChromeDriver with retries and architecture detection
def get_chromedriver_with_retries(max_attempts=3, delay=5):
    attempt = 1
    while attempt <= max_attempts:
        try:
            logger.info(f"Attempt {attempt} to download ChromeDriver...")
            # Detect system architecture
            system_arch = platform.architecture()[0]
            logger.info(f"System architecture: {system_arch}")
            
            # Clean up existing ChromeDriver files and processes
            cleanup_chromedriver()
            
            # Download ChromeDriver with architecture-specific settings
            driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
            logger.info(f"ChromeDriver downloaded successfully to: {driver_path}")
            
            # Verify the downloaded file exists and set permissions
            if not os.path.exists(driver_path):
                raise FileNotFoundError(f"ChromeDriver not found at {driver_path}")
            
            # Set executable permissions
            set_executable_permissions(driver_path)
                
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
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logger.info("ChromeDriver initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize ChromeDriver: {str(e)}")
    sys.exit(1)

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
