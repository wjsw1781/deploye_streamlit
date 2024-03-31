


import os

from pymongo import MongoClient
table_name='douyin_push'

client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')

db = client.zhiqiang_hot
table=db[table_name]


dir=r'C:\projects\py_win\assert\龙珠'


for _id in os.listdir(dir):
    _id_dir=os.path.join(dir,_id)
    if os.path.exists(f"{_id_dir}/ok.mp4"):
        table.update_one({'_id':_id},{'$set':{'ok_mp4':f"{_id_dir}\\ok.mp4"}})
        print(_id)
