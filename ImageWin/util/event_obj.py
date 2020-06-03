from datetime import datetime


class event():
    def __init__(self, name, img_link, time_start, link=None, location=None, time_end=None, event_type=None, content=None):
        self.name = name
        self.img_link = img_link
        self.link = link
        self.location = location
        self.time_start = time_start
        self.time_end = time_end if time_end is not None else time_start
        self.event_type = event_type
        self.isToday = self.is_today()
        self.content = content
        self.json = {
           "name":self.name,
           "img_link":self.img_link,
           "location":self.location,
           "time_start":self.time_start,
           "time_end":self.time_end,
           "event_type": self.event_type,
           "isToday":self.isToday,
           "content":self.content,
           "link":self.link
        }

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        self.isToday = self.is_today()
        return self.json

    @classmethod
    def load(cls, obj:dict):
        return event(name=obj["name"], img_link=obj["img_link"], time_start=obj["time_start"], location=obj["location"],
                     time_end=obj["time_end"], event_type=obj["event_type"], content=obj["content"])

    @classmethod
    def isInDay(cls, target_date: str, start_date: str, end_date: str) -> bool:
        target_date = datetime.strptime(target_date,'%Y/%m/%d')
        start_date = datetime.strptime(start_date,'%Y/%m/%d')
        end_date = datetime.strptime(end_date,'%Y/%m/%d')

        # 判断当前时间是否在范围时间内
        if start_date <= target_date <= end_date:
            return True
        else:
            return False

    def is_today(self) -> bool:
        target_date, start_date, end_date = \
            datetime.today().strftime("%Y/%m/%d"), str(self.time_start), str(self.time_end)
        return self.isInDay(target_date=target_date, start_date=start_date, end_date=end_date)


