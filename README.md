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
    + task_crawler 
        + CrawlerTaskNangang 南港展覽館活動爬蟲
        + CrawlerTaskSongshan 松菸文創活動爬蟲
        + CrawlerTaskHuashan 華山文創活動爬蟲
    + task_pic_maker
    + task_ig

+ SeleniumBot: auto-bot for ig/fb
    + step_login_facebook.py
        + move to facebook.com
        + login in facebook
   + step_movepage_facebook.py
        + move to fans page
   + step_create_post_in_posttool_facebook.py
        + push a post to ins/fb  
+ TaskManger: Task manager, long-term processing tool
+ TinyDBEasy: base on tinyDB, control db by function
