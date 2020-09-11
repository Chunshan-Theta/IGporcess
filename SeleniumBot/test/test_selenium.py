"""
A simple selenium test example written by python
"""

import unittest
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from SeleniumBot.step_create_post_in_posttool_facebook import NewPostInPostToolStep
from SeleniumBot.step_login_facebook import LoginStep
from SeleniumBot.step_movepage_facebook import MovePageToPostToolStep


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--proxy-server={}'.format("118.163.13.200:8080"))
driver = webdriver.Chrome(options=chrome_options,executable_path='/Users/gavinwang/selenium_porcess/SeleniumBot/chromedriver_mac')

latitude, longitude = 23.008332, 120.202711
driver.execute_cdp_cmd("Page.setGeolocationOverride", {
    "latitude": latitude,
    "longitude": longitude,
    "accuracy": 98
})

driver.get('https://mylocation.org')
import time
time.sleep(10)
driver.quit()



