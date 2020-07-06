import re
import time
from datetime import datetime, timedelta

from TinyDBEasy.common import db_tiny
from TaskManger.task_manager import Task
from ImageWin.util.logging_defined import get_logger
from ImageWin.util.config import JPGDIR

from SeleniumBot.driver import FirefoxyDriver, ChromeDriver
from SeleniumBot.step_create_post_in_posttool_facebook import NewPostInPostToolStep
from SeleniumBot.step_login_facebook import LoginStep
from SeleniumBot.step_movepage_facebook import MovePageToPostToolStep
from SeleniumBot.step_util import StepList



class IgAction(object):
    def __init__(self):
        pass
        self.db_name = "ig_action"
        #self.db = db_tiny(db_name="ig_action")

    def remove_punctuation(self, line):
        rule = re.compile("[^ a-zA-Z0-9\u4e00-\u9fa5]")
        line = rule.sub(' ', line)
        return line

    def new_a_post(self, event_name: str, event_information: dict, output: bool = True) -> dict:
        def ig_push(content="我最愛的工作機ＱＱ", img_name="sample.jpg") :
            try:
                driver = FirefoxyDriver().init_driver()

            except:
                driver = ChromeDriver(system_executable_path=False).init_driver()

            driver.set_window_size(360, 1280)
            driver.implicitly_wait(10)
            steps = StepList()

            steps.extend(
                [LoginStep(driver=driver), MovePageToPostToolStep(driver=driver)])
            steps.append(NewPostInPostToolStep(driver=driver, content=content, img_name=img_name))
            print(steps)
            steps.run_over()
            steps.run_over()

            time.sleep(10)
            print(f'OK: Success! event_name:{event_name}, content len: {len(content)}')
            driver.implicitly_wait(15)
            driver.quit()
            return True
        #print(len(main_content_of_the_pos),main_content_of_the_pos)
        main_pic_path = event_information.get('img_link')
        main_link = event_information.get('link')
        event_name_tags_split_by_space = str(" ".join([f"#{i}" for i in self.remove_punctuation(event_name).split()]))
        main_tags = self._generate_date_tag_by_date(
            event_time_start=datetime.strptime(event_information.get('time_start'), "%Y/%m/%d"),
            event_time_end=datetime.strptime(event_information.get('time_end'), "%Y/%m/%d"))
        main_content = f"{event_name} \n {main_link} \n #出遊 #假日 #文青 #活動 #展覽 {event_name_tags_split_by_space} {main_tags}"
        assert len(main_content) < 700, "IG limit number of the post."

        ig_post_obj = {
            "path_of_main_pic_of_the_post": main_pic_path,
            "main_content_of_the_pos": main_content,
            "updated_time": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        content, img_name = main_content, f"{JPGDIR}{event_name}.jpg"
        #print(f"content:{content}, \nimg_name:{img_name}")
        if ig_push(content=content, img_name=img_name):
            with db_tiny(db_name=self.db_name) as db:
                db.insert_by_key(key=event_name, value=ig_post_obj)
        return ig_post_obj

    def new_multi_posts(self, events_name: list, events_information: list) -> list:
        assert len(events_name) == len(events_information), f"len(events_name) need equal to len(events_information), but len(events_name) = {len(events_name)} , len(events_information) = {len(events_information)}"
        results = list()
        for index, (event_name, event_information) in enumerate(zip(events_name, events_information)):
            if index == len(events_name)-1:
                result = self.new_a_post(event_name=event_name, event_information=event_information)
            else:
                result = self.new_a_post(event_name=event_name, event_information=event_information, output=False)

            results.append(result)
        return results

    def has_posted(self, event_name: str) -> bool:
        with db_tiny(db_name=self.db_name) as db:
            token = False if db.find_by_key(key=event_name) is None else True
        return token
    def all(self):
        with db_tiny(db_name=self.db_name) as db:
            all_action = db.find_all()
        return all_action
    def key_exist(self,key)-> bool:
        with db_tiny(db_name=self.db_name) as db:
            return db.key_exist(key=key)
    def _generate_date_tag_by_date(self, event_time_start: datetime, event_time_end: datetime, disabled_daliy_limit=20) -> str:
        #print(event_time_start,event_time_end)
        event_time_start = datetime.now() if datetime.now() > event_time_start else event_time_start
        event_time_end = datetime.now()+timedelta(days=300) if datetime.now()+timedelta(days=300) < event_time_end else event_time_end
        count_cross_days = int((event_time_end-event_time_start).days)
        #print(event_time_start,event_time_end,count_cross_days)
        return_str = list()

        for i in range(count_cross_days+1):
            increase_day = event_time_start + timedelta(days=i)
            event_month_label = f"#{increase_day.strftime('%Y年%m月')}文青活 "
            if event_month_label not in return_str:
                return_str.append(event_month_label)
            if count_cross_days < disabled_daliy_limit:
                return_str.append(f"#{increase_day.strftime('%Y_%m%d')}文青活 ")
        return_str.sort()
        return_str = "".join(return_str)
        #print(return_str)
        return return_str


class IgTaskPush(Task):

    def __init__(self):
        super().__init__(task_label="ig_push")
        self.logging = get_logger(name="TaskIGPush")
        self.task_type = "delay:0.6"
        #self.db_event_information = db_tiny()
        self.db_ig_action = IgAction()

    def task_exe(self, logger_option: bool= False):
        with db_tiny() as db:
            all_post = db.find_all()
            self.logging.info(f"總文章 len: {len(all_post)}")
            self.logging.info(f"已發 len: {len(self.db_ig_action.all())}")
            for event_name, event_information in all_post:
                if not self.db_ig_action.key_exist(key=event_name) and self._ontime(event_information['time_end']):
                    self.logging.info(f"Post: {event_name}")

                    re = IgAction().new_a_post(event_name=event_name, event_information=event_information)
                    if logger_option:
                        self.logging.debug(f"{re}")
                    break

    def task_exe_and_save_result(self, **kwargs):
        self.task_exe(logger_option=True)

    def load_result(self, **kwargs):
        raise NotImplementedError

    def _ontime(self,end_day)->bool:
        end_day = datetime.strptime(end_day, "%Y/%m/%d")
        if datetime.today() <= end_day:
            return True
        else:
            return False


class IgTaskLike(Task):

    def __init__(self):
        super().__init__(task_label="ig_like")
        self.task_type = "delay:2"

    def task_exe(self, **kwargs):
        raise NotImplementedError

    def task_exe_and_save_result(self, **kwargs):
        raise NotImplementedError

    def load_result(self, **kwargs):
        raise NotImplementedError
