# -*- coding: utf-8 -*-
from datetime import timedelta
import sys,os

from loguru import logger
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)

sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(os.path.dirname(os.path.dirname(parent_dir)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(parent_dir))))

os.chdir(basedir)

print('basedir-------------->',basedir)
sys.path.append(basedir)
from DrissionPage import ChromiumOptions,ChromiumPage

edge_path=r"C:\Users\zq\AppData\Local\Microsoft\Edge\Application\msedge.exe"

if __name__ == '__main__':

    ks_user_data=os.path.abspath('./chrome_user_data/ks/')
    ks_uploader="https://cp.kuaishou.com/article/publish/video?origin=www.kuaishou.com"


    co=ChromiumOptions().set_browser_path(edge_path)
    co.set_user_data_path(ks_user_data)
    page=ChromiumPage(co)
    page.get(ks_uploader)



    mp4_path=r'C:\projects\py_win\assert\大型纪录片《普通人的一生3》\video.mp4'
    index_pic=r'C:\projects\py_win\assert\大型纪录片《普通人的一生3》\index.jpg'

# 视频上传逻辑
    page.set.upload_files(mp4_path)
    up_btn=page.ele('t:button@text():上传视频')
    div=up_btn.parent().parent()
    js_code="""
            


            """
    page.run_js()
    up_btn.click()
    page.wait.upload_paths_inputted()
    while 1:
        try:
            ele=page.ele('text=上传成功')
            break
        except Exception as e:
            pass

# 封面逻辑  需要react辅助了 直接使用react的逻辑干就完了
    page.set.upload_files(index_pic)
    bianji_fengmian=page.ele('t:button@text():编辑封面')
    bianji_fengmian.click()
    bianji_fengmian=page.ele('t:div@text()=上传封面')
    bianji_fengmian.click()
# 填写描述
    






    
    input()