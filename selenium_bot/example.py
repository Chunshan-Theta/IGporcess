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

from selenium_bot.driver import FirefoxyDriver, ChromeDriver
from selenium_bot.step_create_post_in_posttool_facebook import NewPostInPostToolStep
from selenium_bot.step_login_facebook import LoginStep
from selenium_bot.step_movepage_facebook import MovePageToPostToolStep
from selenium_bot.step_util import StepList






try:
    driver = FirefoxyDriver().init_driver()

except:
    driver = ChromeDriver(system_executable_path=False).init_driver()

driver.set_window_size(360, 1280)
driver.implicitly_wait(10)
steps = StepList()

steps.extend([LoginStep(driver=driver), MovePageToPostToolStep(driver=driver), NewPostInPostToolStep(driver=driver)])
steps.append(NewPostInPostToolStep(driver=driver,content="我最愛的工作機ＱＱ", img_name="sample.jpg"))
print(steps)
steps.run_over()

time.sleep(10)
print('OK: Success!')
driver.implicitly_wait(15)
driver.quit()