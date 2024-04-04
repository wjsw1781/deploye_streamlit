

from pymongo import MongoClient
#mongodb://root:1213wzwz@139.196.158.152:27017/admin



table_name='longzhuZ'
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot
table=db[table_name]
























