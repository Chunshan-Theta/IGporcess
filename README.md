### env
```
pip install -r requirements.txt
```
```
# update auth
SeleniumBot/auth.py
```


### quick start
```
python app_igpusher.py
```

+ ImageWin : main task script
    + task_crawler import CrawlerTaskNangang, CrawlerTaskSongshan, CrawlerTaskHuashan
    + task_pic_maker import PicTaskMaker
    + task_ig import IgTaskPush

+ SeleniumBot: auto-bot for ig/fb
+ TaskManger: Task manager, long-term processing tool
+ TinyDBEasy: base on tinyDB, control db by function