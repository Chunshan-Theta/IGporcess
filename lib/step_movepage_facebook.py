from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from lib.step_util import Step, DriverStep


class LoginStep(DriverStep):

    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver)

    def run(self) -> bool:
        url = 'https://www.facebook.com/'
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        username, password = "0910365567", "!gavin840511"
        self.find_css_key_input(xpath="input[type='text']", content=username, try_option=True)
        self.find_css_key_input(xpath="input[type='email']", content=username, try_option=True)
        self.find_css_key_input(xpath="input[type='password']", content=password)
        self.driver.implicitly_wait(2)

        # button= driver.find_elements_by_xpath("//*[contains(text(), '登入')]") or driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
        ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        self.driver.implicitly_wait(30)

        assert self.check_element_exist_by_label(label="建立貼文") and self.check_element_exist_by_label(label="平行城市")
        self.status = True
        return self.status





