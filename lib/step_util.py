import time

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, \
    StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

class Step(object):

    def __init__(self):
        self.status = None # None: init, True: success, False: fail

    def run(self) -> tuple:
        raise NotImplementedError


class DriverStep(Step):

    def __init__(self, driver: WebDriver):
        super().__init__()
        self.driver = driver

    def run(self) -> tuple:
        raise NotImplementedError

    def assert_label_element_exist(self,label: str, *args, **kwargs):
        print(f"TRY: check {label}........", end="")
        if self.check_element_exist_by_label(label, *args, **kwargs):
            pass
        else:
            raise AssertionError("element not exist")

    def output_html_file(self, filename='save'):

        with open(f"./{filename}.html", "w") as f:
            f.write(self.driver.page_source)
        self.driver.save_screenshot(filename=f"{filename}.png")
        with open(f"./{filename}.info", "w") as f:
            f.writelines([str(dict_obj)+"\n" for dict_obj in self.driver.get_log("browser")])

        return filename

    def click_button_by_label(self,label: str, max_wait=10, info=True, element_type: str = "*"):
        self.driver.implicitly_wait(10)

        def _by_xpath(timeout=30):
            self.driver.implicitly_wait(timeout)
            if info:
                print(f"INFO: RUN ON PAGE: {self.driver.title}")
            try:

                button_located = WebDriverWait(driver=self.driver, timeout=timeout).until(
                    expected_conditions.presence_of_element_located((By.XPATH, f"//{element_type}[text()='{label}']"))
                )
                return button_located
            except TimeoutException as e:
                print(f"WARRING! can't find button `{label}` in {timeout} sec, output to file:{self.output_html_file(filename=self.driver.title)}.html")
                raise e


        button = _by_xpath()
        current_wait_time_for_element_ready = 0
        while 1:
            try:
                print(f"TRY: click: {label}: {button.text}.......", end='')
                button.click()
                print(f"OK! clicked!")
                break
            except ElementClickInterceptedException:
                button = button.find_element_by_xpath("./..")
                print(f"WARRING! click fail! go to parent element:{button.text}")

            except ElementNotInteractableException as e:  # js of element not ready
                current_wait_time_for_element_ready += 1
                print(
                    f"WARRING! click fail! waited for {current_wait_time_for_element_ready} time,current element: {button.text}, try to find: {label} ")
                time.sleep(1)
                assert current_wait_time_for_element_ready <= max_wait, f"timeout: {e}"
                button = _by_xpath()

            except StaleElementReferenceException as e:  # element is not attached to the page document
                print("WARRING! click fail! element not ready! wait")
                time.sleep(1)
                button = _by_xpath()

    def find_css_key_input(self, xpath, content, try_option=False):
        self.driver.implicitly_wait(2)

        if try_option:
            try:
                field = self.driver.find_element_by_css_selector(xpath)
                field.send_keys(content)
            except:
                pass
        else:
            field = self.driver.find_element_by_css_selector(xpath)
            field.send_keys(content)

    def check_element_exist_by_label(self, label: str, element_type: str = '*') -> bool:
        try:
            _ = self.driver.find_elements_by_xpath(f"//{element_type}[text()='{label}']")
            print(f"OK: Label \'{label}\' exist!")
            return True

        except:
            return False


class StepList(list):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def next_step(self):
        step: Step = self.pop()
        result = step.run()



