from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from auth import username, password
from lib.step_util import Step, DriverStep


class LoginStep(DriverStep):

    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver)

    def run(self) -> bool:
        try:
            url = 'https://www.facebook.com/'
            self.driver.get(url)
            self.driver.implicitly_wait(30)


            self.find_css_key_input(xpath="input[type='text']", content=username, try_option=True)
            self.find_css_key_input(xpath="input[type='email']", content=username, try_option=True)
            self.find_css_key_input(xpath="input[type='password']", content=password)
            self.driver.implicitly_wait(30)

            # button= driver.find_elements_by_xpath("//*[contains(text(), '登入')]") or driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
            ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
            self.driver.implicitly_wait(30)

            self.assert_label_element_exist(label="建立貼文")
            self.assert_label_element_exist(label="平行城市")
            self.status = True
            return self.status
        except Exception as e:
            self.status = False
            raise e








