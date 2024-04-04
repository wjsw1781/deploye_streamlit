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

from huanjie_zhuangtai import Stage,pipeline

longzhu_pip_line=pipeline(name="龙珠处理流程")

# 下载到了本地了   添加封面  按照顺序进行投稿   可以直接投稿  未来很大可能可以抽到ui层进行操作
longzhu_pip_line.add_stage(Stage('下载本地'))
longzhu_pip_line.add_stage(Stage('制作封面'))
longzhu_pip_line.add_stage(Stage('投稿'))


def main_logic(i):
    logger.info(f'开始执行龙珠处理流程---->{i}')

    return True


if __name__ == '__main__':
    current_logic=Stage('制作封面')
    while 1:
        cursor=table.find()
        for i in cursor:

            if 'pipline' not in i:
                i['pipline']=longzhu_pip_line.output_pipeline()

            longzhu_pipline_obj=longzhu_pip_line.restore_pipeline(i['pipline'])
            can_run_flag=longzhu_pipline_obj.can_run_stage_func(current_logic)

            if not can_run_flag:
                continue
            
            try:
                logic_res=main_logic(i)
                longzhu_pipline_obj.change_stage_step_ok(current_logic)
                table.update_one({'_id':i['_id']},{'$set':{'pipline':longzhu_pipline_obj.output_pipeline()}})
            except Exception as e:
                longzhu_pipline_obj.change_stage_step_error(current_logic)

                logger.error(f'龙珠处理流程---->{i["_id"]}出错---->{e}')
                continue





            
         

          