import os
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from SeleniumBot.step_util import Step, DriverStep


class patch_post(dict):

    def get_content(self):
        return self.setdefault("content", "我最愛的工作機ＱＱ")

    def get_img_name(self):
        return self.setdefault("img_name", "sample.jpg")

class NewPostInPostToolStep(DriverStep):

    def __init__(self, driver: WebDriver, content:str = "我最愛的工作機ＱＱ", img_name:str="/Users/gavinwang/selenium_porcess/SeleniumBot/img/sample.jpg"):
        super().__init__(driver=driver)
        self.content = content
        self.img_name = img_name



    def run(self) -> bool:
        init_post_patch = patch_post()
        init_post_patch["content"] = self.content
        init_post_patch["img_name"] = self.img_name
        try:
            self.click_button_by_label(label='建立貼文')
            self.driver.implicitly_wait(10)



            #self.click_button_by_label(label='新增相片')
            #self.driver.implicitly_wait(10)

            """
            ##<input accept="video/*,  video/x-m4v, video/webm, video/x-ms-wmv, video/x-msvideo, video/3gpp, video/flv, video/x-flv, video/mp4, video/quicktime, video/mpeg, video/ogv, .ts, .mkv, image/*, image/heic, image/heif" multiple="" name="composer_photo" display="inline-block" type="file" class="_n _5f0v" id="js_1y">
            ##field = driver.find_element_by_name(name='composer_photo')
            """

            #self.driver.find_element_by_name("composer_photo").send_keys(os.getcwd() + f"/selenium_bot/img/{init_post_patch.get_img_name()}")
            print(init_post_patch.get_img_name())
            self.driver.find_element_by_name("business_composer_photo_uploader").send_keys(f"{init_post_patch.get_img_name()}")
            time.sleep(10)

            self.assert_label_element_exist(label="接收訊息")
            field = self.driver.find_element_by_xpath(f"//*[contains(@aria-label, \"寫點內容\")]")
            field.click()
            field.send_keys(init_post_patch.get_content())
            self.driver.implicitly_wait(10)

            self.click_button_by_label(label='Instagram 動態消息')
            self.driver.implicitly_wait(10)

            self.click_button_by_label(label='發佈', element_type="div")
            self.driver.implicitly_wait(10)

            self.status = True
            return self.status
        except Exception as e:
            self.status = False
            raise e





