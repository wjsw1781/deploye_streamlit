# -*- coding: utf-8 -*-
import datetime
import sys,os
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)
when_import_the_module_the_path=os.path.dirname(__file__)

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

myenv=f'{project_dir}/myenv/Lib/site-packages/'
sys.path.append(myenv)


os.chdir(basedir)

print('basedir-------------->',basedir)
sys.path.append(basedir)

from utils.utils import *
from config import init_one,table,Stage,ther_piplie


#

pipeline_filed='pipeline'
pre=Stage('下载本地')
current_logic=Stage('移除水印和时间轴')


cursor=table.find()
for i in cursor:
    _id=i['_id']
    if 'ok_mp4' not in i:
        table.delete_one({'_id':_id})
        continue
    if i.get('have_up_douyin','')==111:
        print(i['ok_mp4'])
    else:
        logger.error(f'{i["ok_mp4"]}---->没有执行完成')
        table.delete_one({'_id':_id})

    # if 'ok_mp4' in i and len(i['ok_mp4'])>5:
    #     longzhu_pipline_obj=ther_piplie.restore_pipeline(i[pipeline_filed])

    #     longzhu_pipline_obj.change_stage_step_ok(pre)
    #     longzhu_pipline_obj.change_stage_step_ok(current_logic)

    #     table.update_one({'_id':i['_id']},{'$set':{pipeline_filed:longzhu_pipline_obj.output_pipeline(),'have_up_douyin':111}})
    #     logger.success(f'{_id}---->执行完成')
    # else:
        # print('没有ok_mp4','mid' in i)

logger.success(f'{current_logic}---->执行完成')







            
         

          