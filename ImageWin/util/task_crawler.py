import datetime
import json
import os
import requests as rq
from bs4 import BeautifulSoup
from ImageWin.util.config import LOGDIR
from ImageWin.util.event_obj import event
from TaskManger.task_manager import Task


class CrawlerTask(Task):
    def __init__(self,task_label, task_type="delay:1"):
        super().__init__(task_label=task_label)
        self.task_type = task_type

    def task_exe(self, **kwargs) -> list:
        raise NotImplementedError

    def task_exe_and_save_result(self, date=datetime.datetime.now()) -> str:
        event_objs = self.task_exe(date=date)

        # initiate log file
        filename = f"{LOGDIR}{self.task_label}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        # dump to file
        print(f"save: {filename}")
        self.latest_log_file = filename
        assert isinstance(event_objs, list)
        save_file = open(filename, "w+")
        json.dump(event_objs, save_file, ensure_ascii=False)

        return filename

    @classmethod
    def load_result(cls, filename) -> dict:
        assert filename is not None, "Not pointed to the log file"
        return json.load(open(filename, "r"))

    @classmethod
    def get_one_data(cls,skip:int = 0) -> dict:
        filenames = os.listdir(f"{LOGDIR}")
        filename = filenames[skip] if skip < len(filenames) else filenames[0]
        return json.load(open(f"{LOGDIR}{filename}", "r"))


class CrawlerTaskNangang(CrawlerTask):

    def __init__(self):
        super().__init__(task_label="CrawlerTask_Nangang")

    def task_exe(self, date=datetime.datetime.now()) -> list:
        #
        re_event_objs = []

        #
        # @# print(date.year,date.month,date.day)
        year = date.year
        month = date.month

        #
        url = "https://www.tainex1.com.tw/calendar/index?type=&year={}&month={}&page=1".format(year, month)
        html = rq.get(url=url, timeout=10)
        beauty_html_obj = BeautifulSoup(html.content, 'html.parser')
        # print(beauty_html_obj)

        #
        events_list_obj = beauty_html_obj.find(id="events_list")
        # print(events_list_obj)

        #
        events_info = events_list_obj.find_all(class_="events_info")
        events_img = events_list_obj.find_all(class_="events_img")
        events_link = events_list_obj.find_all(class_="list_link")
        for e_info, e_img, e_link_obj in zip(events_info, events_img, events_link):

            ## title
            event_title = e_info.find(class_="title article").string

            ## location
            event_location = "南港展覽館" #+ e_info.find(class_="location").string

            ## event time
            tags_p = e_info.find_all("p")
            event_time_arr = []
            for p in tags_p:
                # print(p.attrs,len(p.attrs),p.string)
                if len(p.attrs) == 0:
                    event_time_arr.append(p.string)

            if event_time_arr[0].count("/") == 1:  # 缺少年份
                test_date0_1 = datetime.datetime.strptime("{}/{}".format(year + 1, event_time_arr[0]), '%Y/%m/%d')
                test_date0_2 = datetime.datetime.strptime("{}/{}".format(year, event_time_arr[0]), '%Y/%m/%d')
                test_date0_3 = datetime.datetime.strptime("{}/{}".format(year - 1, event_time_arr[0]), '%Y/%m/%d')
                checked_data0 = test_date0_1 if abs(test_date0_1 - date) <= abs(
                    test_date0_2 - date) else test_date0_2 if abs(test_date0_2 - date) <= abs(
                    test_date0_3 - date) else test_date0_3
                event_time_arr[0] = checked_data0.strftime('%Y/%m/%d')

            if event_time_arr[1].count("/") == 1:  # 缺少年份
                test_date1_1 = datetime.datetime.strptime("{}/{}".format(year + 1, event_time_arr[1]), '%Y/%m/%d')
                test_date1_2 = datetime.datetime.strptime("{}/{}".format(year, event_time_arr[1]), '%Y/%m/%d')
                test_date1_3 = datetime.datetime.strptime("{}/{}".format(year - 1, event_time_arr[1]), '%Y/%m/%d')
                checked_data1 = test_date1_1 if abs(test_date1_1 - date) <= abs(
                    test_date1_2 - date) else test_date1_2 if abs(test_date1_2 - date) <= abs(
                    test_date1_3 - date) else test_date1_3
                event_time_arr[1] = checked_data1.strftime('%Y/%m/%d')
            # @# print(event_time_arr)

            #
            e_img_link = "https://www.tainex1.com.tw" + e_img.attrs['src']
            e_link = "https://www.tainex1.com.tw" + e_link_obj.attrs['href']

            #
            re_event_objs.append(
                event(name=event_title, img_link=e_img_link, link=e_link, location=event_location,
                      time_start=event_time_arr[0],
                      time_end=event_time_arr[1]).to_dict())

            #
            # @# print("+"*20)
        return re_event_objs


class CrawlerTaskSongshan(CrawlerTask):

    def __init__(self):
        super().__init__(task_label="CrawlerTask_Songshan")

    def task_exe(self, date=datetime.datetime.now()) -> list:
        #
        re_event_objs = []

        #
        url = f"https://www.songshanculturalpark.org/helper.aspx?q=dayevent&date={date.strftime('%Y/%m/%d')}"
        events_obj = json.loads(rq.get(url=url).content)
        for e in events_obj:
            date_str = e['Date']
            time_start = date_str[:10]
            time_end = date_str[11:]
            eid = e['ID']
            event_pic = e['HomeImageFileName']
            link = f"https://www.songshanculturalpark.org/Exhibition.aspx?ID={e['ID']}"

            #
            url = "https://www.songshanculturalpark.org/Exhibition.aspx?q=get&ID=" + eid
            event_detail = json.loads(rq.get(url=url, timeout=10).content)
            try:
                bigpic = event_detail['item'][0]['TitleImage']
                event_pic = eid + '/' + bigpic
            except IndexError as error:
                pass
                ## print(error)

            #
            re_event_objs.append(
                event(name=e['Title'], img_link="https://www.songshanculturalpark.org/images/" + event_pic,
                      time_start=time_start,
                      time_end=time_end, location="松山文創園區", link=link).to_dict())

        return re_event_objs


class CrawlerTaskHuashan(CrawlerTask):

    def __init__(self):
        super().__init__(task_label="CrawlerTask_Huashan")

    def task_exe(self, date=datetime.datetime.now()) -> list:
        #
        re_event_objs = []

        # @# print(date.year,date.month,date.day)
        year = date.year
        month = date.month

        #
        url = "https://www.huashan1914.com/w/huashan1914/exhibition?index=1"
        html = rq.get(url=url, timeout=10)
        beauty_html_obj = BeautifulSoup(html.content, 'html.parser')
        # print(beauty_html_obj)

        #
        events = beauty_html_obj.find_all(class_="item-static")
        for e in events:

            e_link = f"https://media.huashan1914.com/{e.a.attrs['href']}"
            e_title = (e.find(class_="card-text-name").string.strip("\n"))
            e_date = (e.find(class_="event-date").text.strip("\n")).split(" - ")
            e_img_link = (e.find(class_="card-img").attrs["style"][len("background-image:url("):-1])
            e_type = (e.find(class_="event-list-type").text.strip("\n"))

            #
            e_date_start = e_date[0]
            e_date_start = str(e_date_start).replace(".", "/")
            e_date_end = e_date[1] if len(e_date) > 1 else e_date[0]
            e_date_end = str(e_date_end).replace(".", "/")
            if e_date_start.count("/") == 1:  # 缺少年份
                test_date0_1 = datetime.datetime.strptime("{}/{}".format(year + 1, e_date_start), '%Y/%m/%d')
                test_date0_2 = datetime.datetime.strptime("{}/{}".format(year, e_date_start), '%Y/%m/%d')
                test_date0_3 = datetime.datetime.strptime("{}/{}".format(year - 1, e_date_start), '%Y/%m/%d')
                checked_data0 = test_date0_1 if abs(test_date0_1 - date) <= abs(
                    test_date0_2 - date) else test_date0_2 if abs(test_date0_2 - date) <= abs(
                    test_date0_3 - date) else test_date0_3
                e_date_start = checked_data0.strftime('%Y/%m/%d')

            if e_date_end.count("/") == 1:  # 缺少年份
                test_date1_1 = datetime.datetime.strptime("{}/{}".format(year + 1, e_date_end), '%Y/%m/%d')
                test_date1_2 = datetime.datetime.strptime("{}/{}".format(year, e_date_end), '%Y/%m/%d')
                test_date1_3 = datetime.datetime.strptime("{}/{}".format(year - 1, e_date_end), '%Y/%m/%d')
                checked_data1 = test_date1_1 if abs(test_date1_1 - date) <= abs(
                    test_date1_2 - date) else test_date1_2 if abs(test_date1_2 - date) <= abs(
                    test_date1_3 - date) else test_date1_3
                e_date_end = checked_data1.strftime('%Y/%m/%d')

            #
            # @# print("+"*20)

            #
            re_event_objs.append(
                event(name=e_title, img_link=e_img_link, location="華山1914", time_start=e_date_start,
                      time_end=e_date_end, event_type=e_type, link=e_link).to_dict())
        return re_event_objs