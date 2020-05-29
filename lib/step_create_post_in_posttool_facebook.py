from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from lib.step_util import Step, DriverStep


class MovePageToPostToolStep(DriverStep):

    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver)

    def run(self) -> bool:
        try:
            self.click_button_by_label(label='平行城市')
            self.driver.implicitly_wait(10)

            assert self.check_element_exist_by_label(label="發佈工具")

            self.click_button_by_label(label='發佈工具')
            self.driver.implicitly_wait(10)
            assert self.check_element_exist_by_label(label="觸及人數")

            self.status = True
            return self.status
        except Exception as e:
            self.status = False
            raise e





