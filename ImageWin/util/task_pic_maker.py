from ImageWin.util.frame_base import EventLineFrame1Img1Text
from TinyDBEasy.common import db_tiny
from TaskManger.task_manager import Task
import os
from ImageWin.util.config import PNGDIR
from urllib3.exceptions import ReadTimeoutError

class PicTaskMaker(Task):
    def __init__(self):
        super().__init__(task_label="pic_Maker")
        self.task_type = "delay:0.2"
        #self.db = db_tiny()
        if not os.path.exists(f"{PNGDIR}"):
            os.makedirs(f"{PNGDIR}")
        self.exists_file = os.listdir(f"{PNGDIR}")

    def task_exe(self,subfilename:str ="jpg", **kwargs):
        with db_tiny() as db:
            for name, data in db.find_all():
                if f"{name}.{subfilename}" not in self.exists_file:
                    try:
                        self.logging.info(f"saving...{name} - {data['img_link']}")
                        image_title = data['location']
                        a = EventLineFrame1Img1Text(image_title=image_title, img_dir=data['img_link'],
                                                    content=f"{data['name']}\n{data['time_start'].replace('/','')}"
                                                    f"-{data['time_end'].replace('/','')}")
                        a_img = a.stack_2_image()
                        if subfilename == "jpg":
                            a_img = a_img.convert("RGB")
                        a_img.save(f"{PNGDIR}{name}.{subfilename}")
                        self.logging.info(f"save: {PNGDIR}{name}.{subfilename}")
                    except ReadTimeoutError as e:
                        self.logging.warning(e)
                    except Exception as e:
                        self.logging.error(e)
                        raise e
                else:
                    print(f"{name}.png exists")

    def task_exe_and_save_result(self, **kwargs):
        self.task_exe()



