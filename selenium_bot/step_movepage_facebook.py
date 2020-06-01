from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from selenium_bot.step_util import Step, DriverStep


class MovePageToPostToolStep(DriverStep):

    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver)

    def run(self) -> bool:
        try:
            self.click_button_by_label(label='平行城市')
            self.driver.implicitly_wait(10)

            self.assert_label_element_exist(label="發佈工具")

            self.click_button_by_label(label='發佈工具')
            self.driver.implicitly_wait(10)
            self.assert_label_element_exist(label="已發佈的貼文")

            self.status = True
            return self.status
        except Exception as e:
            self.status = False
            raise e





