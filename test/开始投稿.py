# -*- coding: utf-8 -*-
import re
import sys,os
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)

project_dir=basedir 
# 遍历所有父节点目录 如果存在readme.md文件 就返回那个目录
while True:
    if os.path.exists(os.path.join(project_dir, 'readme.md')):
        break
    project_dir = os.path.dirname(project_dir)
    if project_dir==os.path.dirname(project_dir):
        raise ValueError('未找到项目根目录')


sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(os.path.dirname(os.path.dirname(parent_dir)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(parent_dir))))

os.chdir(basedir)

print('basedir-------------->',basedir)
sys.path.append(basedir)


from concurrent.futures import ThreadPoolExecutor
import time

import json
import re
from DrissionPage import ChromiumOptions,SessionPage,ChromiumPage
from loguru import logger


user_data_dir=f'{project_dir}/user_data/douyin/'
os.makedirs(user_data_dir,exist_ok=True)
co=ChromiumOptions().set_user_data_path(user_data_dir)
# co=ChromiumOptions().headless().set_user_data_path(user_data_dir)
page = ChromiumPage(co)
page.get('https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page')
page.wait.doc_loaded()

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
    index_img=data['index_img']
    index_id=data['index_id']

    desc='来源于阿b的欣酱_由于某奇异发力___阿b不给力_导致下架_非常可惜_希望抖音能够坚挺_最后_如果喜欢请给原作者_二重转生的欣酱_支持___'
    title=f"龙珠Z_第{index_id}集_re"


    try:
        # 触发上传
        btn_ele=page.ele('t:input@@name=upload-btn@@type=file',timeout=10).next(index=1)
        page.set.upload_files(ok_mp4)
        btn_ele.click()
        page.wait.upload_paths_inputted()
  

        # 选择封面
        page.set.upload_files(index_img)
        # page.ele('xpath://div[@text=选择封面]').click()
        # page.ele('t:div@@text:上传封面').click()
        # page.ele('t:div@@text:上传封面').click()
        # page.ele('xpath://div[@class="semi-upload-drag-area"]').click()

        # page.wait.upload_paths_inputted()

        # 填写描述 简介  标题
        page.ele('xpath://input[@placeholder="好的作品标题可获得更多浏览"]').input(title)
        page.ele('xpath://div[@data-placeholder="添加作品简介"]').input(desc)

        # 点击发布

        logger.success(index_id)
        table.update_one({'_id':_id},{'$set':{'step':ok_status,'index_id':index_id}})
    except Exception as e:
        logger.error(f'{index_id}    {e }')



if __name__ == '__main__':
    from_status=6
    temp_status=7
    ok_status=8
    other_status=18
    error_status=18

    max_work = 1
    executor = ThreadPoolExecutor(max_work)

    table.update_many({'step':temp_status},{'$set':{'step':from_status}})
    table.update_many({'step':error_status},{'$set':{'step':from_status}})
    # table.update_many({'step':ok_status},{'$set':{'step':from_status}})
    index_id=0
    while 1:
        if executor._work_queue.qsize()  > max_work:
            time.sleep(10)
            continue
        
        data=table.find_one_and_update(
                                {'step':from_status,'index_id':index_id},
                                {'$set':{'step':temp_status}}
                                    )
        index_id+=1
        if not(data):
            logger.error(f'队列空----> {index_id}.mp4 还没有下载')
            time.sleep(1)
            continue

        _id=data['_id']
        executor.submit(process, data)

    executor.shutdown(wait=True)

    logger.info(' control c  ----> ')
    logger.info('<----  退出线程池  ----> ')
    os._exit(0)
