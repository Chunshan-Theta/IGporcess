import os

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, \
    StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

def click_button_by_label(label:str,max_wait =10):
    def _by_xpath() -> webdriver.remote.webelement.WebElement:
        driver.implicitly_wait(10)
        return driver.find_elements_by_xpath(f"//*[text()='{label}']")

    button = _by_xpath()
    button = button[0]
    current_wait_time_for_element_ready = 0
    while 1:
        try:
            print(f"try click: {label}")
            button.click()
            #time.sleep(10)
            break
        except ElementClickInterceptedException:
            button = button.find_element_by_xpath("./..")
            print(f"go to parent element:{button.text}")

        except ElementNotInteractableException as e: # js of element not ready
            #print(driver.page_source)
            current_wait_time_for_element_ready += 1
            print(f"waited for {current_wait_time_for_element_ready},current element: {button.text}, try to find: {label} ")
            time.sleep(1)
            assert current_wait_time_for_element_ready <= max_wait, f"timeout: {e}"
            button = _by_xpath()
            button = button[0]

        except StaleElementReferenceException as e: #element is not attached to the page document
            print("element not ready! wait")
            time.sleep(1)
            button = _by_xpath()
            button = button[0]









chrome_options = webdriver.ChromeOptions()

# show windows or not
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')

#mobile mode
#chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')


# disable notifications
prefs = {
    'profile.default_content_setting_values' :
        {
        'notifications' : 2
         }
}
chrome_options.add_experimental_option('prefs',prefs)

driver = webdriver.Chrome(executable_path='./lib/chromedriver', chrome_options=chrome_options) if os.path.exists('./lib/chromedriver') else webdriver.Chrome(chrome_options=chrome_options)
driver.set_window_size(360, 1280)
driver.implicitly_wait(10)

url = 'https://www.facebook.com/'
driver.get(url)
driver.implicitly_wait(10)


username, password = "0910365567", "!gavin840511"
field = driver.find_element_by_css_selector("input[type='text']")
field.send_keys(username)
field = driver.find_element_by_css_selector("input[type='email']")
field.send_keys(username)
field = driver.find_element_by_css_selector("input[type='password']")
field.send_keys(password)
driver.implicitly_wait(2)

#button= driver.find_elements_by_xpath("//*[contains(text(), '登入')]") or driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
driver.implicitly_wait(30)





click_button_by_label(label='平行城市')
driver.implicitly_wait(10)

click_button_by_label(label='發佈工具')
driver.implicitly_wait(10)

click_button_by_label(label='建立貼文')
driver.implicitly_wait(10)



click_button_by_label(label='相片／影片')
driver.implicitly_wait(10)


<input accept="video/*,  video/x-m4v, video/webm, video/x-ms-wmv, video/x-msvideo, video/3gpp, video/flv, video/x-flv, video/mp4, video/quicktime, video/mpeg, video/ogv, .ts, .mkv, image/*, image/heic, image/heif" multiple="" name="composer_photo" display="inline-block" type="file" class="_n _5f0v" id="js_1y">

stop
field = driver.find_element_by_name(name='composer_photo')
driver.implicitly_wait(10)



button=driver.find_elements_by_xpath("//*[contains(text(), '稍後再說')]")
if len(button) > 0:
    button[0].click()

driver.implicitly_wait(5)

button=driver.find_elements_by_xpath("//*[contains(text(), 'Cancel')]")
if len(button) > 0:
    button[0].click()
button=driver.find_elements_by_xpath("//*[contains(text(), '取消')]")
if len(button) > 0:
    button[0].click()

driver.implicitly_wait(5)

button = driver.find_elements_by_css_selector('[aria-label="New Post"]')
if len(button) > 0:
    button[0].click()
button = driver.find_elements_by_css_selector('[aria-label="新貼文"]')
if len(button) > 0:
    button[0].click()
driver.implicitly_wait(2)

os.system('autokey-run -s select_image')
driver.implicitly_wait(10)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Expand')]")
if len(button) > 0:
    button[0].click()
    driver.implicitly_wait(10)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")
button[0].click()

driver.implicitly_wait(10)
field = driver.find_elements_by_tag_name('textarea')[0]
field.click()
description = 'hello World!'
field.send_keys(description)

driver.implicitly_wait(15)
button=driver.find_elements_by_xpath("//*[contains(text(), 'Share')]")
button[-1].click()


print('Success!')
driver.implicitly_wait(15)
driver.quit()