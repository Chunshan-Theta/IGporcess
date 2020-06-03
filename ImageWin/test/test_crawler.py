from ImageWin.util.task_crawler import CrawlerTaskNangang, CrawlerTaskSongshan, CrawlerTaskHuashan


a = CrawlerTaskNangang()
print(a.task_exe_and_save_result())

a = CrawlerTaskSongshan()
print(a.task_exe_and_save_result())

a = CrawlerTaskHuashan()
print(a.task_exe_and_save_result())