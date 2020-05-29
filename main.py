import os

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, \
    StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import time

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from lib.step_create_post_in_posttool_facebook import NewPostInPostToolStep
from lib.step_login_facebook import LoginStep
from lib.step_movepage_facebook import MovePageToPostToolStep


class ChromeDriver(object):

    def __init__(self, system_executable_path=True):

        options = webdriver.ChromeOptions()

        # mobile mode
        # chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')

        # disable window
        options.add_argument('--headless')
        # disable notifications
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                }
        }
        options.add_experimental_option('prefs', prefs)
        if system_executable_path:
            print("INFO: using system driver")
            self.driver = webdriver.Chrome(options=options)
        else:
            print("INFO: using local driver")
            self.driver = webdriver.Chrome(options=options, executable_path=f'{os.getcwd()}/lib/chromedriver_mac')
    def init_driver(self):
        return self.driver





try:
    driver = ChromeDriver(system_executable_path=False).init_driver()

except:
    driver = ChromeDriver().init_driver()

driver.set_window_size(360, 1280)
driver.implicitly_wait(10)
step = LoginStep(driver=driver)
step.run()


step = MovePageToPostToolStep(driver=driver)
step.run()

step = NewPostInPostToolStep(driver=driver)
step.run()

time.sleep(10)
print('OK: Success!')
driver.implicitly_wait(15)
driver.quit()