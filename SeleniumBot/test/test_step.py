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


class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self, ):
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options, executable_path='/Users/gavinwang/selenium_porcess/SeleniumBot/chromedriver_mac')

        self.driver.implicitly_wait(10)

    def tearDown(self):
        """Stop web driver"""
        self.driver.quit()

    def test_case_1(self):
        LoginStep(self.driver).run()
        MovePageToPostToolStep(self.driver).run()
        NewPostInPostToolStep(self.driver).run()
    def test_case_2(self):
        latitude, longitude = 23.008332, 120.202711
        self.driver.execute_cdp_cmd("Page.setGeolocationOverride", {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": 98
        })

        LoginStep(self.driver).run()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
    unittest.TextTestRunner(verbosity=2).run(suite)




