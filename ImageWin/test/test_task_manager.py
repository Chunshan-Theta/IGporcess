from TaskManger import TaskManager
from ImageWin.util.task_crawler import CrawlerTaskNangang, CrawlerTaskSongshan, CrawlerTaskHuashan

manager = TaskManager()
task = CrawlerTaskNangang()
#task.task_type="delay:0.03"

manager.add_task(task_obj=task)
manager.add_task(task_obj=CrawlerTaskSongshan())
manager.add_task(task_obj=CrawlerTaskHuashan())

manager.loop_run()