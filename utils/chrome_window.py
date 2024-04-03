

# -*- coding: utf-8 -*-
import sys,os
import time
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

print('project_dir---->',project_dir)



from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage._pages.chromium_tab import ChromiumTab



def get_one_window_with_out_proxy(chrome_user_data_dir):

    pid_user_data_path=os.path.abspath(f'{project_dir}/user_data/{chrome_user_data_dir}/')
    os.makedirs(pid_user_data_path, exist_ok=True)

    co = ChromiumOptions().auto_port().set_user_data_path(pid_user_data_path)
    co.headless()
    co.headless(False)
    co.set_retry(0)
    co.set_pref(arg='profile.default_content_settings.popups', value='0')
    co.set_argument('--hide-crash-restore-bubble')
    page = ChromiumPage(co)
    page.set.window.max()
    return page


if __name__ == '__main__':
    chrome_user_data_dir="dy_up"
    page = get_one_window_with_out_proxy(chrome_user_data_dir)
    url='https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page'

    chrome:ChromiumPage=get_one_window_with_out_proxy(chrome_user_data_dir=chrome_user_data_dir)

    workder_tab=chrome.new_tab(url)

    mp4_path=r'd:\projects\deploy_streamlit\spider_up_topic\assert\大型纪录片\大型纪录片_百日誓师大会上吃席_\video.mp4good.mp4'

    workder_tab.set.upload_files(mp4_path)
    up_btn=workder_tab.ele("@@text()=或直接将视频文件拖入此区域").parent()
    if not up_btn:
        raise ValueError("上传按钮未找到")
    up_btn.click()

    workder_tab.wait.upload_paths_inputted()
