from ImageWin.util.task.task_db import DbTaskUpdateLoop
from ImageWin.util.task.task_manager import TaskManager
from ImageWin.util.task_crawler import CrawlerTaskNangang, CrawlerTaskSongshan, CrawlerTaskHuashan
from ImageWin.util.task_pic_maker import PicTaskMaker

manager = TaskManager()
manager.add_task(task_obj=DbTaskUpdateLoop())


manager.loop_run()