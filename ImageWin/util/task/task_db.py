import json
import os.path
from typing import Optional

from ImageWin.util.config import LOGDIR, DBDIR
from os import path
from ImageWin.util.task_crawler import CrawlerTask
from ImageWin.util.task.task_manager import Task


class db(object):
    def __init__(self,db_save_path=None, db_name = "db_event_information"):
        db_save_path = DBDIR if db_save_path is None else db_save_path
        self.db_dir = f"{db_save_path}{db_name}.json"
        if path.exists(self.db_dir):
            #print("loading DB")
            self.db = json.load(fp=open(self.db_dir, "r+"))
        else:
            #print("creating DB")
            self.db = {}
            self.output2file()

    def output2file(self) -> None:
        json.dump(obj=self.db, fp=open(self.db_dir, "w+"), ensure_ascii=False)

    def loading_logfile(self):
        logfiles = os.listdir(f"{LOGDIR}")
        logfiles = [path for path in logfiles if path.endswith("json")]
        logfiles.sort()
        # print(logfiles)
        for logfile in logfiles:

            try:
                objs = CrawlerTask.load_result(filename=f"{LOGDIR}{logfile}")
                for obj in objs:
                    if obj['name'] not in self.db:
                        self.insert_by_key(key=self.key_filter(obj['name']), value=obj)
            except json.decoder.JSONDecodeError as e:
                print(f"log file error: {logfile},{e}")

    def insert_by_key(self, key: str, value: dict) -> Optional[str]:
        """
        insert a new data.
        return Null if the key is exist.

        :param key:
        :param value:
        :return:
        """
        key_filterify = self.key_filter(key=key)
        if key_filterify in self.db:
            return None
        self.db[key_filterify] = value
        return key

    def find_by_key(self, key: str) -> Optional[dict]:
        """
        Get data by key search.
        return None if key isn't exist.

        :param key:
        :return:
        """
        key_filterify = self.key_filter(key=key)
        if key_filterify not in self.db:
            return None
        return self.db[key_filterify]

    def update_by_key(self, key: str, column: str, value) -> bool:
        """
        updated a value of column.

        :param key:
        :param column:
        :param value:
        :return: return True or False for symbol of success or not
        """

        key_filterify = self.key_filter(key=key)
        if key_filterify not in self.db:
            return False
        if column not in db[key_filterify]:
            return False

        self.db[key_filterify][column] = value
        return True

    def delete_by_key(self, key: str, column: str):
        self.db[self.key_filter(key=key)][column] = None

    def find_all(self) -> list:
        return [(key, val) for key, val in self.db.items()]

    @classmethod
    def key_filter(cls, key: str) -> str:
        disable_symbols =[".", "/", "|", "-", "\\", "?", "\"", "｜", "*", ":", ">", "<"]
        for symbol in disable_symbols:
            key = key.replace(symbol, "_")

        return key


class DbTaskUpdateLoop(Task):
    def __init__(self, task_type="delay:1.5"):
        super().__init__(task_label="db")
        self.task_type = task_type
        self.db = db()

    def task_exe(self):
        self.db.loading_logfile()

    def task_exe_and_save_result(self) -> str:
        self.task_exe()
        self.db.output2file()
        return self.db.db_dir
