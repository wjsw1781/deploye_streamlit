

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



def get_one_window_with_out_proxy(item_name):

    pid_user_data_path=os.path.abspath(f'{project_dir}/user_data/{item_name}/')
    os.makedirs(pid_user_data_path, exist_ok=True)

    co = ChromiumOptions().auto_port().set_user_data_path(pid_user_data_path)
    co.headless()
    co.headless(False)
    co.set_retry(0)
    co.set_pref(arg='profile.default_content_settings.popups', value='0')
    co.set_argument('--hide-crash-restore-bubble')
    page = ChromiumPage(co)
    page.set.window.max()
    time.sleep(5)
    return page
