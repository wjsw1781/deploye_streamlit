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
from config import *

# 环节状态

from huanjie_zhuangtai import pipeline,Stage

wx_gzh=aio_save_media_by_wx()

def main_logic(i):
    _id=i['_id']
    title=i['title']
    bvid=i['bvid']
    aid=i['aid']
    title=i['title']

    local_mp4=i.get('local_mp4',None)
    shuiyin_positon_rate=i.get('shuiyin_positon_rate',None)
    shijianzhou_part=i.get('shijianzhou_part',None)
    if local_mp4 is None or shuiyin_positon_rate is None or shijianzhou_part is None:
        raise ValueError(f'参数不够 shuiyin_positon_rate {shuiyin_positon_rate}  shijianzhou_part  {shijianzhou_part} 前面有阶段应该是人工那边没进行时间轴水印标注')
    
    ok_mp4=os.path.abspath(local_mp4+"ok.mp4")
    logger.info(f' {ok_mp4}  ---->即将产生这个中间文件 但马上就会被重命名为twice_confirm 水印移除操作')
    ok_mp4_twice_confirm=ok_mp4+"twice_confirm.mp4"

    #两次确认 因为那个工具失败了也会产生视频 
    if not os.path.exists(ok_mp4_twice_confirm):
        crop_video_top_ratio(local_mp4,ok_mp4,shuiyin_positon_rate,shijianzhou_part)
        os.rename(ok_mp4,ok_mp4_twice_confirm)

    table.update_one({'_id':i['_id']},{'$set':{'ok_mp4':ok_mp4_twice_confirm}})
    logger.success(f'{current_logic}')
    return True
if __name__ == '__main__':
    ther_piplie=pipeline()
    current_logic=Stage('移除水印和时间轴')

    pipeline_filed='pipeline'


    while 1:
        cursor=table.find()
        for i in cursor:
            _id=i['_id']

            try:
                longzhu_pipline_obj=ther_piplie.restore_pipeline(i[pipeline_filed])
                can_run_flag=longzhu_pipline_obj.can_run_stage_func(current_logic)
            except Exception:
                continue

            if not can_run_flag:
                continue
            
            try:
                title=i['title']+"\n"
                logger.info(title)
                main_logic(i)

                longzhu_pipline_obj.change_stage_step_ok(current_logic)
                
            except Exception as e:
                longzhu_pipline_obj.change_stage_step_error(current_logic,str(e))

                logger.error(f'处理流程{title}---->出错---->{e}')
                continue

            table.update_one({'_id':i['_id']},{'$set':{pipeline_filed:longzhu_pipline_obj.output_pipeline()}})

        logger.success(f'{current_logic}---->执行完成')
        time.sleep(100)







            
         

          