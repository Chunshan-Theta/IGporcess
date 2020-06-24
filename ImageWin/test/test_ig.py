from TaskManger import TaskManager
from ImageWin.util.task_ig import IgTaskPush

manager = TaskManager()
manager.add_task(task_obj=IgTaskPush())

manager.loop_run()