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


def main_logic(i):
    _id=i['_id']
    title=i['title']
    index=i['index']

    fix_title=title.split('来源于')[0]
    # 制作封面
    src_img=os.path.abspath('./龙珠封面.png')
    index_img_local_path=f"./fengmian/{_id}.jpg"
    os.makedirs(os.path.dirname(index_img_local_path),exist_ok=True)

    index_desc=f"""龙珠z_re {index} \n {fix_title}"""

    image_add_text(src_img,index_desc,index_img_local_path)
    table.update_one({'_id':i['_id']},{'$set':{'index_img_local_path':index_img_local_path}})
    logger.success(f'龙珠封面制作完成---->{fix_title}')
    return True
if __name__ == '__main__':
    longzhu_pip_line=pipeline()
    current_logic=Stage('制作封面')
    pipeline_filed='pipeline'


    while 1:
        cursor=table.find()
        for i in cursor:

            longzhu_pipline_obj=longzhu_pip_line.restore_pipeline(i[pipeline_filed])
            can_run_flag=longzhu_pipline_obj.can_run_stage_func(current_logic)

            # if not can_run_flag:
            #     continue
            
            try:
                title=i['title']+"\n"
                title=title.replace('_','\n')

                logic_res=main_logic(i)
                if not logic_res:
                    raise ValueError('失败 由于是多线程运行错误无法打印')
                longzhu_pipline_obj.change_stage_step_ok(current_logic)
                table.update_one({'_id':i['_id']},{'$set':{pipeline_filed:longzhu_pipline_obj.output_pipeline()}})
            except Exception as e:
                longzhu_pipline_obj.change_stage_step_error(current_logic,str(e))

                logger.error(f'龙珠处理流程---->{i["_id"]}出错---->{e}')
                continue

        logger.success(f'{current_logic}---->执行完成')
        time.sleep(100)







            
         

          