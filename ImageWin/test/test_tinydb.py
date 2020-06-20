from tinydb import TinyDB, Query
from tinydb.table import Table

db = TinyDB('./test_tinydb.json')
db.drop_table(name='user_table')
table = db.table('user_table')


query = Query()
#search
def basic_cond(db,requirements):
    for column,cond,value in requirements:
        if column not in db:
            return False
        if cond == '==' and not db[column]==value:
            return False
        if cond == '!=' and not db[column]!=value:
            return False
        if cond == '>' and not db[column] > value:
            return False
        if cond == '<' and not db[column] < value:
            return False
        if cond == '>=' and not db[column] >= value:
            return False
        if cond == '<=' and not db[column] <= value:
            return False
        if cond == 'substring' or cond == 'contain':
            try:
                str(db[column]).index(value)
            except Exception:
                return False
    return True


def search_human(target_db:Table,requirements:[tuple]):
    return target_db.search(lambda db: basic_cond(db,requirements))

def update_human(update_fields:dict,target_db:Table,requirements:[tuple]):
    return target_db.update(fields=update_fields,cond=lambda db: basic_cond(db, requirements))

def delete_human(target_db:Table,requirements:[tuple]):
    return target_db.remove(cond=lambda db: basic_cond(db, requirements))

def insert_human(target_db:Table,row:dict):
    return target_db.insert(row)
def insert_mulit_human(target_db:Table,rows:[dict]):
    for row in rows:
        insert_human(target_db=target_db,row=row)

# insert
insert_mulit_human(target_db=table,rows=[
    {'name': 'John', 'age': 30},
    {'name': 'theta', 'age': 10},
    {'name': 'gavin', 'age': 60},
    {'name': 'gavin', 'age': 45}
])
print(table.all())


# search
requirements=[
    ('name','contain','gavin'),
    ('age','>',10)
]
print(search_human(target_db=table,requirements=requirements))

# update
update_fields={
    "age": 100,
    "name": "gavin_convert"
}
update_human(update_fields=update_fields,target_db=table,requirements=requirements)
print(table.all())


# delete
requirements=[
    ('name','contain','John')
]
delete_human(target_db=table,requirements=requirements)
print(table.all())

table.update({"age":0},table.eid == 2)
print(table.all())
