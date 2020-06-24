from TaskManger import db_tiny
import json
db = db_tiny(db_name="unit_test")
db.drop_all()

json_obj:dict = json.load(open('ig_action.json','r'))

for key,val in json_obj.items():
    print(key,val)
    db.insert_by_key(key=key,value=val)

