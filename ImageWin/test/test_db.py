from ImageWin.util.task.task_db import db

a = db()
a.loading_logfile()

a.output2file()


key = "本質展 -./|\-\\?\"*:>< 生活飾物"
assert db.key_filter(key=key) == "本質展 _____________ 生活飾物", db.key_filter(key=key)