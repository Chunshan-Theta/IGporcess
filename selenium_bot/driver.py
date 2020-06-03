from selenium import webdriver
import os

class ChromeDriver(object):

    def __init__(self, system_executable_path=True):

        options = webdriver.ChromeOptions()

        # mobile mode
        # chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')

        # reduced the memory utilization
        options.add_argument("-js-flags=--expose-gc");
        # disable window
        #options.add_argument('--headless')
        # disable notifications
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                }
        }
        options.add_experimental_option('prefs', prefs)
        if system_executable_path:
            print("INFO: using system driver Chrome")
            self.driver = webdriver.Chrome(options=options)
        else:
            print("INFO: using local driver Chrome")
            self.driver = webdriver.Chrome(options=options, executable_path=f'{os.getcwd()}/selenium_bot/chromedriver_mac')
    def init_driver(self):
        return self.driver


class FirefoxyDriver(object):

    def __init__(self):


        options = webdriver.FirefoxOptions()
        options.add_argument(argument='--headless')


        print("INFO: using local driver: Firefoxy")
        print("INFO: using system driver: Firefoxy")
        self.driver = webdriver.Firefox(options=options)
    def init_driver(self):
        return self.driver