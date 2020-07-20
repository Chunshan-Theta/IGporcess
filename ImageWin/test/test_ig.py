from ImageWin.util.task_ig import IgTaskPush, IgTaskPushLastDay
from TaskManger.task_manager import TaskManager

manager = TaskManager()
manager.add_task(task_obj=IgTaskPush())

manager.loop_run()