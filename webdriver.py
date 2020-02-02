# File for opening up Selenium driver for videos, music, etc.
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Get file paths and set up the webdriver for controlling the browser
ADBLOCK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "driver", "adblock.crx")
CHROME_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "driver", "chromedriver.exe")

chrome_options = Options()
chrome_options.add_extension(ADBLOCK_PATH)
chrome_options.add_argument('start-maximized')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROME_DRIVER_PATH)
print("SETTING DRIVER POSITION")
driver.set_window_position(-10000,-10000)
print("SWITCHING TABS")
driver.switch_to.window(driver.window_handles[0])