
from ImageWin.util.task_crawler import CrawlerTaskNangang, CrawlerTaskSongshan, CrawlerTaskHuashan
from ImageWin.util.task_pic_maker import PicTaskMaker
from ImageWin.util.task_ig import IgTaskPush, IgTaskPushLastDay
from TaskManger.task_manager import TaskManager
from TinyDBEasy.common import DbTaskUpdateLoop

manager = TaskManager()
manager.add_task(task_obj=IgTaskPush())
manager.add_task(task_obj=IgTaskPushLastDay())
manager.add_task(task_obj=PicTaskMaker())
manager.add_task(task_obj=DbTaskUpdateLoop())
manager.add_task(task_obj=CrawlerTaskNangang())
manager.add_task(task_obj=CrawlerTaskSongshan())
manager.add_task(task_obj=CrawlerTaskHuashan())


manager.loop_run()