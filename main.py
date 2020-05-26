import os

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys







chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

driver = webdriver.Chrome(executable_path='./lib/chromedriver', chrome_options=chrome_options)
#driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_window_size(360, 640)
driver.implicitly_wait(10)

url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
driver.get(url)
driver.implicitly_wait(10)


username, password = "taipei.ev", "gavin84"
field = driver.find_element_by_css_selector("input[type='text']")
field.send_keys(username)
field = driver.find_element_by_css_selector("input[type='password']")
field.send_keys(password)
driver.implicitly_wait(2)

#button= driver.find_elements_by_xpath("//*[contains(text(), '登入')]") or driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()



driver.implicitly_wait(5)

button=driver.find_elements_by_xpath("//*[contains(text(), 'Not Now')]")
if len(button) > 0:
    button[0].click()

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