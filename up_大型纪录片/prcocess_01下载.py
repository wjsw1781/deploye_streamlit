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
from config import init_one,table

# 环节状态

from huanjie_zhuangtai import pipeline,Stage

wx_gzh=aio_save_media_by_wx()

def main_logic(i):
    _id=i['_id']
    title=i['title']
    bvid=i['bvid']
    aid=i['aid']
    title=i['title']
    fix_title="".join(html_to_lxml(title).xpath('.//text()'))

    four_wx_imgs=i.get('four_wx_imgs',[])
    safe_dir_name=get_safe_title(fix_title)
    local_mp4=f"./assert/{safe_dir_name}_{_id}/{safe_dir_name}.mp4"
 

    os.makedirs(os.path.dirname(local_mp4),exist_ok=True)

    if not os.path.exists(local_mp4):
        flag=download_video_sync(bvid,aid,local_mp4)
        time.sleep(10)
    if four_wx_imgs==[]:
        four_imgs=extract_four_frames(local_mp4)
        for fram_local_path in four_imgs:
            data=wx_gzh._upload_local_media_to_wx_https(fram_local_path)
            url=data[1]
            four_wx_imgs.append(url)

    table.update_one({'_id':i['_id']},{'$set':{'local_mp4':local_mp4,'four_wx_imgs':four_wx_imgs}})
    logger.success(f'下载完成---->{safe_dir_name}')
    return True
if __name__ == '__main__':
    ther_piplie=pipeline('大型纪录片处理流程')
    current_logic=Stage('下载本地')
    pipeline_filed='pipeline'


    while 1:
        cursor=table.find()
        for i in cursor:
            _id=i['_id']
            if pipeline_filed not in i:
                init_one(_id)
                time.sleep(3)
                continue

            longzhu_pipline_obj=ther_piplie.restore_pipeline(i[pipeline_filed])
            can_run_flag=longzhu_pipline_obj.can_run_stage_func(current_logic)

            if not can_run_flag:
                continue
            
            try:
                title=i['title']+"\n"
                logger.info(title)

                main_logic(i)

                longzhu_pipline_obj.change_stage_step_ok(current_logic)
                
            except Exception as e:
                longzhu_pipline_obj.change_stage_step_error(current_logic,str(e))

                logger.error(f'处理流程---->{title}出错---->{e}')
                continue

            table.update_one({'_id':i['_id']},{'$set':{pipeline_filed:longzhu_pipline_obj.output_pipeline()}})

        logger.success(f'{current_logic}---->执行完成')
        time.sleep(10)







            
         

          