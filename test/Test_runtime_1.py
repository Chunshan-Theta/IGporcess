import unittest
import time
import random
import sys
import os
print(os.getcwd())
sys.path.append(os.getcwd()[:os.getcwd().rfind("/")])
from TinyDBEasy.common import db_tiny

class MyTestCase(unittest.TestCase):
    def test_new(self):
        db = db_tiny(db_name="unittest", db_save_path="./")
        db.drop_all()
        while len(db.find_all()) < 10:
            if random.random()> 0.5:
                try:
                    db.insert_by_key(key=str(len(db.find_all())+1),value={'data':"QQ"})
                except Exception as e:
                    print(e)
            time.sleep(1)

        db.close()




if __name__ == '__main__':
    unittest.main()
