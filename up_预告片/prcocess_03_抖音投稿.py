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
    title=i['title']

    ok_mp4=i.get('ok_mp4',None)
    if not(ok_mp4) :
        raise ValueError(f'参数不够 前面的阶段没把这个阶段环节所需要的数据准备好')
    dir_name=os.path.dirname(ok_mp4)
    if os.path.exists(f'{dir_name}/{_id}'):
        return True
    # 打开抖音投稿页面
    title=os.path.basename(ok_mp4.replace('ok.mp4',''))

    workder_tab=chrome.new_tab(url)
    time.sleep(15)
    # 上传视频
    workder_tab.set.upload_files(ok_mp4)
    up_btn=workder_tab.ele("@@text()=或直接将视频文件拖入此区域").parent()
    if not up_btn:
        raise ValueError("上传按钮未找到")
    up_btn.click()
    while not(workder_tab.wait.upload_paths_inputted()):
        logger.info("等待上传完成")
        pass

    # 填写标题
    @retry(max_attempts=5, delay=2)
    def write_tile():
        up_btn=workder_tab.ele("@@placeholder=好的作品标题可获得更多浏览")
        if not up_btn:
            raise ValueError("上传按钮未找到")
        up_btn.input(title)
        return True

    flag2=write_tile()

    # 填写简介
    @retry(max_attempts=5, delay=2)
    def write_desc():
        up_btn=workder_tab.ele("@@data-placeholder=添加作品简介")
        if not up_btn:
            raise ValueError("描述元素")
        up_btn.input(title+_id)
        return True
    flag3=write_desc()

        # 点击上传
    @retry(max_attempts=50, delay=10)
    def click_up():
        if 'content/manage' in workder_tab.url:
            return True
        up_btn=workder_tab.ele("@@text()=发布")
        if not up_btn:
            raise ValueError("上传按钮未找到")
        up_btn.click()
        current_url=workder_tab.url
        if 'enter_from=publish_page' in current_url:
            raise ValueError("还没有跳转")
        return True
    flag4=click_up()
    workder_tab.close()

    if not (flag2 and flag3 and flag4):
        raise ValueError(f"上传失败操作过程中失败了 flag2 {flag2} flag3 {flag3} flag4 {flag4}")

    # 创建一个空文件表明已经上传过了
    with open(f'{dir_name}/{_id}','w') as f:
        f.write('')

    logger.success(f'---->{title}  完成')

    return True

if __name__ == '__main__':
    ther_piplie=pipeline()
    current_logic=Stage('抖音投稿')
    pipeline_filed='pipeline'

    chrome_user_data_dir="dy_up"
    chrome=get_one_window_with_out_proxy(chrome_user_data_dir=chrome_user_data_dir)
    url='https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page'


    while 1:
        cursor=table.find()
        for i in cursor:
            _id=i['_id']

            try:
                longzhu_pipline_obj=ther_piplie.restore_pipeline(i[pipeline_filed])
                can_run_flag=longzhu_pipline_obj.can_run_stage_func(current_logic)
            except Exception as e:
                continue

            if not can_run_flag:
                continue
            
            try:
                title=i['title']+"\n"

                main_logic(i)

                longzhu_pipline_obj.change_stage_step_ok(current_logic)
                
            except Exception as e:
                longzhu_pipline_obj.change_stage_step_error(current_logic,str(e))

                logger.error(f'处理流程{title}---->出错---->{e}')
                continue

            table.update_one({'_id':i['_id']},{'$set':{pipeline_filed:longzhu_pipline_obj.output_pipeline()}})

        logger.success(f'{current_logic}----------------------------->执行完成')
        time.sleep(600)


          