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
def retry(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Attempt {attempts + 1} failed:", e)
                    attempts += 1
                    time.sleep(delay)
            return False
        return wrapper
    return decorator

def main_logic(i):
    _id=i['_id']
    title=i['title']
    index=i['index']
    index_img_local_path=i['index_img_local_path']
    local_mp4=i['local_mp4']
    safe_title=i.get('safe_title',None)
    desc=i.get('desc',None)
    if desc==None:
        raise ValueError("还没有转码完成")
    if len(desc.replace('_','') )<5:
        desc+=f"自b的欣酱 某奇异发力 阿b顶不住,导致下架,发现ks可以投稿成功,现在试试抖音 喜欢请支持 二重转生的欣酱"
    workder_tab=chrome.new_tab(url)
    time.sleep(5)
    # 上传视频
    workder_tab.set.upload_files(local_mp4)
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
        up_btn.input(safe_title)
        return True

    flag2=write_tile()

    # 填写简介
    @retry(max_attempts=5, delay=2)
    def write_desc():
        up_btn=workder_tab.ele("@@data-placeholder=添加作品简介")
        if not up_btn:
            raise ValueError("描述元素")
        up_btn.input(desc+_id)
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
        raise ValueError("上传失败操作过程中失败了")
    logger.success(f'---->{current_logic}  完成')
    return True


if __name__ == '__main__':
    longzhu_pip_line=pipeline()
    current_logic=Stage('投稿')

    pipeline_filed='pipeline'
    chrome_user_data_dir="dy_up"
    chrome=get_one_window_with_out_proxy(chrome_user_data_dir=chrome_user_data_dir)
    url='https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page'



    while 1:
        for i in range(1,300):
            i=table.find_one({'index':i})
            if not i:
                continue

            longzhu_pipline_obj=longzhu_pip_line.restore_pipeline(i[pipeline_filed])
            can_run_flag=longzhu_pipline_obj.can_run_stage_func(current_logic)

            if not can_run_flag:
                continue
            
            try:
                title=i['title']
                index=i['index']
                logger.info(f'---->{title}  开始执行')
                main_logic(i)

                
                longzhu_pipline_obj.change_stage_step_ok(current_logic)
            except Exception as e:
                longzhu_pipline_obj.change_stage_step_error(current_logic,str(e))

                logger.error(f'龙珠处理流程---->{index}出错---->{e}')
                
            table.update_one({'_id':i['_id']},{'$set':{pipeline_filed:longzhu_pipline_obj.output_pipeline()}})

        logger.success(f'{current_logic}---->执行完成')
        time.sleep(100)







            
         

          