
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
# -i https://pypi.tuna.tsinghua.edu.cn/simple 



item_name="dy_up"

from utils.utils import *



chrome:ChromiumPage=get_one_window_with_out_proxy(item_name=item_name)


url='https://creator.douyin.com/creator-micro/content/manage'

merge_to_mp4_file=r"D:\projects\deploy_streamlit\spider_up_topic\assert\大型纪录片\大型纪录片_普通人的一生2_\video.mp4good.mp4"
merge_to_mp4_file=r"C:\projects\py_win\assert\龙珠\0a77385138e1a816bcdd246a6dee88c5\ok.mp4"
title="龙珠z_re"
description="龙珠z_re_永远热爱"
index_local=r'C:\projects\py_win\assert\封面\龙珠封面.png3.png'

workder_tab=chrome.new_tab(url)

for i in range(10):
    time.sleep(3)
    # 证明react成功加载
    root=workder_tab.ele('xpath://div[@id="root"]')
    all_upload_video=workder_tab.eles('@class:video-card--')

    if root and all_upload_video :
        break

for ii in all_upload_video:
    title=ii.ele('@class:info-title-text--').text
    status=ii.ele('@class:info-status').text
    time_up=ii.ele('@class:info-time').text
    change_fengmian=ii.ele('@text()=修改描述和封面')
    change_fengmian=workder_tab.ele('xpath://div[@class="semi-upload-drag-area"]')

    if change_fengmian:
        workder_tab.set.upload_files(merge_to_mp4_file)
        change_fengmian.click()
        workder_tab.wait.upload_paths_inputted()
        
    logger.success(f'{title}  {status}  {time_up}')



# 设置要上传的文件
for i in range(10):
    #证明可以被点击触发视频上传框 
    up_input=workder_tab.ele('xpath://input[@accept="video/mp4,video/x-m4v,video/*"]')

    up_buton=up_input.parent()
    if up_buton:
        break
workder_tab.set.upload_files(merge_to_mp4_file)
up_buton.click() 
workder_tab.wait.upload_paths_inputted()



# 标题
title_input=workder_tab.ele('xpath://input[@placeholder="好的作品标题可获得更多浏览"]')
title_input.input(title)
# 描述
description_input=workder_tab.ele('xpath://*[@data-placeholder="添加作品简介"]')
description_input.input(description)

# 发布按钮
while 1:
    publish_buton=workder_tab.ele('xpath://button[text()="发布"]')
    time.sleep(10)
    if 'manage' in workder_tab.url:
        logger.success(workder_tab.url)
        break
    try:
        publish_buton.click()
    except Exception:
        pass


# if __name__ == '__main__':
#     try:
#         main_up_fun()

#     except Exception as e:
#         tell_to_wx("上传抖音失败  "+str(e))
    


    