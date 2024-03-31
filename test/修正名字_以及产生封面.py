# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
import re
import sys,os
import time
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)

sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(os.path.dirname(os.path.dirname(parent_dir)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(parent_dir))))

os.chdir(basedir)

print('basedir-------------->',basedir)
sys.path.append(basedir)





from loguru import logger
from redisbloom.client import Client
from pymongo import MongoClient
import redis 
#mongodb://root:1213wzwz@139.196.158.152:27017/admin

table_name='douyin_push'
table_detail=f'{table_name}_detail'

client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')

db = client.zhiqiang_hot
table=db[table_name]
from utils.utils import *

def process(data):
    _id=data['_id']
    ok_mp4=data['ok_mp4']
    name=os.path.basename(ok_mp4)


    try:
        index=name.split('集_')[0].split('_')[0]
        index_id=int(index)
        index_img_text = f"龙珠Z ## {index_id} "
        other_line=name.split('来源于')[0]
        other_line=re.sub(r'_{1,}', "_", other_line)
        other_line="\n".join(other_line.split('_'))
        index_img_text+='\n'+other_line
        index_img_text=index_img_text.strip()
        index_img_text=index_img_text.replace('.mp4',"")
        if '篇' not in index_img_text:
            index_img_text+='篇'
        image_path = r"C:\projects\py_win\assert\封面\龙珠封面.png"
        output_path = image_path+f"{index_id}.png"

        image_add_text(image_path,index_img_text, output_path)


        table.update_one({'_id':_id},{'$set':{'step':ok_status,'index_id':index_id,"index_img":output_path}})
        logger.success(index_img_text)
    except Exception as e:
        logger.error(f"https://www.kuaishou.com/short-video/{clientCacheKey}")



if __name__ == '__main__':
    from_status=4
    temp_status=5
    ok_status=6
    other_status=166
    error_status=16

    max_work = 1
    executor = ThreadPoolExecutor(max_work)

    table.update_many({'step':temp_status},{'$set':{'step':from_status}})
    table.update_many({'step':ok_status},{'$set':{'step':from_status}})

    while 1:
        if executor._work_queue.qsize()  > max_work:
            time.sleep(10)
            continue

        data=table.find_one_and_update(
                                {'step':from_status},
                                {'$set':{'step':temp_status}}
                                    )
        if not(data):
            logger.error(f'队列空')
            time.sleep(100)
            continue

        _id=data['_id']
        clientCacheKey=data['clientCacheKey']

        executor.submit(process, data)

    executor.shutdown(wait=True)

    logger.info(' control c  ----> ')
    logger.info('<----  退出线程池  ----> ')
    os._exit(0)
