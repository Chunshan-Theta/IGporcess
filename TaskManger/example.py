from TaskManger import DbTaskUpdateLoop
from TaskManger import TaskManager

manager = TaskManager()
manager.add_task(task_obj=DbTaskUpdateLoop())


manager.loop_run()