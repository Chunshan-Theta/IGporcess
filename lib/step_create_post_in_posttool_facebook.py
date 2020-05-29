import os
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from lib.step_util import Step, DriverStep


class NewPostInPostToolStep(DriverStep):

    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver)

    def run(self) -> bool:
        try:
            self.click_button_by_label(label='建立貼文')
            self.driver.implicitly_wait(10)

            self.assert_label_element_exist(label="接收訊息")
            field = self.driver.find_element_by_xpath(f"//*[contains(@aria-label, \"撰寫貼文\")]")
            field.click()
            field.send_keys("我最愛的工作機ＱＱ")
            self.driver.implicitly_wait(10)

            self.click_button_by_label(label='相片／影片')
            self.driver.implicitly_wait(10)

            """
            ##<input accept="video/*,  video/x-m4v, video/webm, video/x-ms-wmv, video/x-msvideo, video/3gpp, video/flv, video/x-flv, video/mp4, video/quicktime, video/mpeg, video/ogv, .ts, .mkv, image/*, image/heic, image/heif" multiple="" name="composer_photo" display="inline-block" type="file" class="_n _5f0v" id="js_1y">
            ##field = driver.find_element_by_name(name='composer_photo')
            """

            self.driver.find_element_by_name("composer_photo").send_keys(os.getcwd() + "/lib/img/sample.jpg")
            time.sleep(10)

            self.click_button_by_label(label='貼文將會顯示在 Instagram')
            self.driver.implicitly_wait(10)

            self.click_button_by_label(label='立即分享', element_type="span")
            self.driver.implicitly_wait(10)

            self.status = True
            return self.status
        except Exception as e:
            self.status = False
            raise e





