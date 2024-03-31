# -*- coding: utf-8 -*-
from datetime import timedelta
import sys,os
import time

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
from DrissionPage._pages.chromium_tab import ChromiumTab

edge_path=r"C:\Users\zq\AppData\Local\Google\Chrome\Application\chrome.exe"

user_data=os.path.abspath('./chrome_user_data/dy/')
os.makedirs(user_data,exist_ok=True)
uploader_url="https://creator.douyin.com/creator-micro/content/upload"
# uploader_url="https://cp.kuaishou.com/article/publish/video"



from pymongo import MongoClient

table_name='douyin_push'
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')

db = client.zhiqiang_hot
table=db[table_name]


co=ChromiumOptions().set_browser_path(edge_path)
co.set_user_data_path(user_data)
co.set_timeouts(page_load=60)
page=ChromiumPage(co)
worker_tab=page.new_tab(uploader_url)





# 快手上传逻辑
def kuaishou(worker_tab:ChromiumTab):
    # 视频上传逻辑
    worker_tab.set.upload_files(ok_mp4)
    up_btn=worker_tab.ele('xpath://label')
    up_btn.click()
    worker_tab.wait.upload_paths_inputted()
    print(up_btn)

# 封面逻辑  需要react辅助了 直接使用react的逻辑干就完了
    page.set.upload_files(index_img)
    bianji_fengmian=page.ele('t:button@text():编辑封面')
    bianji_fengmian.click()
    bianji_fengmian=page.ele('t:div@text()=上传封面')
    bianji_fengmian.click()
    pass

# 抖音上传逻辑
def dy_uploader(worker_tab:ChromiumTab,ok_mp4,index_img):
    # 视频上传逻辑
    worker_tab.set.upload_files(ok_mp4)
    up_btn=worker_tab.ele('xpath://label')
    print(up_btn.extra_result)
    up_btn.click()
    worker_tab.wait.upload_paths_inputted()

# 封面逻辑  需要react辅助了 直接使用react的逻辑干就完了
    page.set.upload_files(index_img)
    bianji_fengmian=page.ele('t:button@text():编辑封面')
    bianji_fengmian.click()
    bianji_fengmian=page.ele('t:div@text()=上传封面')
    bianji_fengmian.click()
    pass
if __name__ == '__main__':

    from_status=4
    temp_status=from_status+1
    ok_status=temp_status+1
    error_status=ok_status+10
    
    table.update_many({'step':temp_status},{'$set':{'step':from_status}})

    for index_id in range(9,291):
        data=table.find_one_and_update(
                                {'step':from_status,'index_id':index_id},
                                {'$set':{'step':temp_status}}
                                    )
        if not(data):
            logger.error(f'队列空')
            time.sleep(1)
            continue

        _id=data['_id']
        index_img=data['index_img']
        ok_mp4=r"C:\Users\zq\Videos\2024-01-08 22-31-21.mkv"
        dy_uploader(worker_tab,ok_mp4,index_img)



    # 填写描述
    