import datetime
import time
import requests
from ImageWin import util


class Task(object):

    def __init__(self, task_label):
        self.task_type = "once"
        self.stage = "init"
        self.task_label = task_label
        self.latest_log_file = None
        self.logging = util.logging_defined.get_logger(name="unitTask")

    def task_exe(self, **kwargs):
        raise NotImplementedError

    def task_exe_and_save_result(self, **kwargs):
        raise NotImplementedError


# Manager
class TaskManager(object):

    def __init__(self):
        self.task_list = list()
        self.delay_task_list = list()
        self.logging = util.logging_defined.get_logger(name="TaskManager")

    def loop_run(self, timedelta = 1):
        while len(self.task_list) > 0 or len(self.delay_task_list) > 0:
            self.logging.debug(f"run:{self.manager_status()}")
            self.run()
            time.sleep(timedelta)

    def run(self, save2file=True) -> bool:

        try: # check delay task stage
            assert len(self.delay_task_list) > 0, "pass stage: empty_delay_task_list"
            if len(self.delay_task_list) > 0:
                for task_obj, runtime in self.delay_task_list.copy():
                    if datetime.datetime.now() > runtime:

                        # add job to taskline
                        self.logging.debug(f"add job:{task_obj.task_label}")
                        self.task_list.append(task_obj)

                        # del job from waited taskline
                        del_index = self.delay_task_list.index((task_obj, runtime))
                        self.logging.debug(f"del waited job:{self.delay_task_list[del_index][0].task_label}")
                        del self.delay_task_list[del_index]
        except AssertionError as e:
            pass#print(str(e))

        except Exception as e:
            #print(f"Unknow Error (check delay task stage): {str(e)},{type(e)}")
            self.logging.exception(f"Unknow Error (check delay task stage): {str(e)},{type(e)},{e.with_traceback()}")

        try: # run stage
            assert len(self.task_list) > 0, "pass stage: empty_task_list"
            # initiate task
            now_task: Task = self.task_list.pop()
            self.logging.info(f"task_label:{now_task.task_label}")

            now_task.stage = "pop"


            # run the task
            now_task.task_exe_and_save_result() if save2file else now_task.task_exe()
            # finished the task
            now_task.stage = "finished"
            if now_task.task_type == "forever":
                self.task_list.append(now_task)
                now_task.stage = "re_init"
            if 'delay' in now_task.task_type:
                delay_hr = float(now_task.task_type[now_task.task_type.find(":")+1:]) if ":" in now_task.task_type else 1
                self.add_delay_task(task_obj=now_task, delay_hr=delay_hr)
                self.logging.debug(f"add job to waited line:{now_task.task_label}")

            return True

        except ValueError as e:
            self.logging.exception(f"ValueError Error: {now_task.task_type},task_type is wrong,{str(e)}")
        except requests.exceptions.ReadTimeout as e:
            self.logging.exception(f"TimeOutError Error: {now_task.task_label},Get HTML Time Out,{str(e)}")
        except AssertionError as e:
            pass#self.logging.exception(str(e))

        except Exception as e:
            self.logging.exception(f"Unknow Error (run stage): {str(e)},{type(e)}")

        return False

    def add_delay_task(self, task_obj: Task, delay_hr: float):
        delay_unit = (task_obj, datetime.datetime.now()+datetime.timedelta(minutes=int(60*delay_hr)))
        self.delay_task_list.append(delay_unit)

    def add_task(self,task_obj: Task):
        self.task_list.append(task_obj)

    def manager_status(self):
        task_list = "Task list: "
        for task in self.task_list:
            task_list += f"{task.task_label}"
            task_list += ", "
        task_list = task_list[:-2]

        delay_task_list = "delay Task list: "
        for task, nexttimestamp in self.delay_task_list:
            nexttimestamp: datetime.datetime
            delay_task_list += f"{task.task_label}:{nexttimestamp.strftime('%Y/%m/%d %H:%M:%S')}"
            delay_task_list += ", "
        delay_task_list = delay_task_list[:-2]

        return f"\"self.task_list\": \"{task_list}\",\"self.delay_task_list\": \"{delay_task_list}\""
