from ImageWin.util.task.task_db import db_tiny

db = db_tiny(db_name="unit_test")
db.drop_all()


key = "本質展 -./|\-\\?\"*:>< 生活飾物"
assert db.key_filter(key=key) == "本質展 _____________ 生活飾物", db.key_filter(key=key)


# insert
row=[
    {'name': 'John', 'age': 30},
    {'name': 'theta', 'age': 10},
    {'name': 'gavin', 'age': 60},
    {'name': 'gavin', 'age': 45}
]
for idx,dict_value in enumerate(row):
    db.insert_by_key(key=str(idx),value=dict_value)
print("insert",db.find_all())


# search
print("search",db.find_by_key(key="0"))


# update
update_fields={
    "age": 100,
    "name": "gavin_convert"
}
db.update_by_key(key="0",column="age",value=100)
print("update",db.find_all())


# delete
db.delete_by_key(key="0")
print("delete",db.find_all())


