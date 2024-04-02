
# -*- coding: utf-8 -*-
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

from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage._pages.chromium_tab import ChromiumTab


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


item_name="dy_up"

# 上传抖音
def up_to_dy():
    from_step=video_item.is_human_ok
    end_step=video_item.is_tougao_success
    error_step=video_item.is_tougao_success+video_item.error_reason
    for ii in table_two.find({'step':from_step}):
        try:
            _id=ii['_id']
            safe_title=ii['safe_title']
            local_name = os.path.abspath(f'./assert/{kind}/{safe_title}')
            pic_index = f"{local_name}/index.jpg"
            video_mp4_name = f"{local_name}/video.mp4"
            video_mp4_namegood = video_mp4_name + "good.mp4"

            table_two.update_one({'_id':_id},{'$set':{"step":end_step},})

            logger.success(f"{curent_time}  {safe_title}  投稿过程  __-----__  完成")
        except Exception as e:
            table_two.update_one({'_id':_id},{'$set':{"step":error_step,'error_reason':"裁剪 投稿过程中出错"+str(e)}})



    pass


from utils.utils import *


def main_up_fun():

    pass


chrome:ChromiumPage=get_one_window_with_out_proxy(item_name=item_name)


url='https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page'

merge_to_mp4_file=r"D:\projects\deploy_streamlit\spider_up_topic\assert\大型纪录片\大型纪录片_普通人的一生2_\video.mp4good.mp4"

index_local_path='D:\projects\deploy_streamlit\spider_up_topic\assert\大型纪录片\大型纪录片_普通人的一生2_\index.jpg'

title="大型纪录片_普通人的一生2_"

desc="永远热爱| 牛马| 无奈"

workder_tab=chrome.new_tab(url)

# 触发上传视频按钮
@retry(max_attempts=5, delay=2)
def up_video_func():
    up_btn=workder_tab.ele("@@text()=点击上传")
    if not up_btn:
        raise ValueError("上传按钮未找到")
    workder_tab.set.upload_files(merge_to_mp4_file)
    up_btn.click()
    workder_tab.wait.upload_paths_inputted()
    return True

flag1=up_video_func()

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
    up_btn.input(desc)
    return True
flag3=write_desc()

# 修正封面
@retry(max_attempts=5, delay=2)
def fix_index_img():
    if not(workder_tab.ele("@@text()=选择封面").click()):
        raise ValueError("选择封面未找到")
    time.sleep(2)
    
    if not(workder_tab.ele("@@text()=上传封面").click() ):
        raise ValueError("上传封面按钮未找到")
    time.sleep(2)

    workder_tab.set.upload_files(index_local_path)
    workder_tab.ele("@@text()=点击上传 或直接将图片文件拖入此区域").parent().click()
    time.sleep(2)
    workder_tab.wait.upload_paths_inputted()
    ok_ele=workder_tab.ele("@@text()=重新选择").next()
    
    if ok_ele.text!="完成":
        raise ValueError("没有最终非共面判定元素!")

    return  True

flag33=fix_index_img()

# 点击上传
@retry(max_attempts=20, delay=10)
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

if flag1 and flag2 and flag3 and flag4:
    logger.success(f" {title}  投稿  __-----__  完成")
else:
    logger.error(f" {title}  投稿  __-----__  完成")






input()


# if __name__ == '__main__':
#     try:
#         main_up_fun()

#     except Exception as e:
#         tell_to_wx("上传抖音失败  "+str(e))
    


    