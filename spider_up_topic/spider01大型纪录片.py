# -*- coding: utf-8 -*-
import datetime
import re
import sys,os

from pymongo import MongoClient
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)

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

os.chdir(basedir)

print('basedir-------------->',basedir)
sys.path.append(basedir)

import requests

from utils import bilibili
from item_status import Vidoe_Item_Status
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot
from utils.utils import *

video_item=Vidoe_Item_Status()
# 总共操纵两个表 一个所有发布这种视频的up主 id  一个是所有视频id
table_one=db['daxingjilupian_ups']
table_two=db['daxingjilupian_videos']

item={
    'uid':498421499,
    'key':498421499,
    'up_name':"我是李四儿",
    '_id':md5(498421499),
}
table_one.update_one({'_id':item['_id']},{'$set':item},upsert=True)

# 入库 下载  抽帧  质检  投稿

def into_db():
    add_count=0
    uids =list(table_one.find())

    for recorder in uids:
        uid=recorder['uid']
        uid=int(uid)
        all_video = bilibili.get_all_videos_sync(uid, 3)

        good_video = list(filter(lambda x: x['play'] > 10000, all_video))

        for video in good_video:
            safe_title = get_safe_title(video['title'])
            bvid = video['bvid']
            aid = video['aid']
            item = {
                "_id":md5(bvid),
                **video,
                "shuiyin_bili":0,
                "shijianzhou_delete_length":0,
                "new_shuiyin_bili":0,
                "new_shijianzhou_delete_length":0,
                "safe_title":safe_title,
                "step":video_item.is_spider_to_db,
            }
            table_two.update_one({'_id':item['_id']},{'$set':item},upsert=True)
            add_count+=1
    
    return add_count


def download_video():
    wx_gzh=aio_save_media_by_wx()

    from_step=video_item.is_spider_to_db
    end_step=video_item.is_download_local
    error_step=end_step+video_item.error_reason

    table_two.update_many({'step':error_step},{'$set':{'step':from_step}})
    # table_two.update_many({'step':end_step},{'$set':{'step':from_step}})

    for ii in table_two.find({'step':from_step}):
        try:
            _id=ii['_id']
            bvid=ii['bvid']
            aid=ii['aid']
            safe_title=ii['safe_title']
            local_name = os.path.abspath(f'./assert/大型纪录片/{safe_title}')
            os.makedirs(local_name, exist_ok=True)
            pic_index = f"{local_name}/index.jpg"
            video_mp4_name = f"{local_name}/video.mp4"
            # 人工质检后的最终产出
            video_mp4_namegood = video_mp4_name + "good.mp4"
            pic_index_url = ii['pic']
            # 下载封面
            with open(pic_index, 'wb') as ff:
                ff.write(requests.get(pic_index_url).content)

            # 下载视频
            if not(os.path.exists(video_mp4_name)):
                flag = bilibili.download_video_sync(bvid=bvid, aid=aid, filename=video_mp4_name)
                if not (flag):
                    raise ValueError(f"下载视频失败  bvid  {bvid}")

            # 抽帧
            all_wx_frame_pic_urls=[]
            if 'all_wx_frame_pic_urls' not in ii :
                all_frame_pick = bilibili.extract_four_frames(video_mp4_name)
                if len(all_frame_pick)!=4:
                    raise ValueError(f"抽帧失败  bvid  {bvid}")

                # pic_frames=[for i in all_frame_pick]
                try:
                    for fram_local_path in all_frame_pick:
                        data=wx_gzh._upload_local_media_to_wx_https(fram_local_path)
                        url=data[1]
                        all_wx_frame_pic_urls.append(url)
                except Exception as e:
                    pass
            
            table_two.update_one({'_id':_id},{'$set':{"step":end_step,'all_wx_frame_pic_urls':all_wx_frame_pic_urls}})
            logger.success(f"{curent_time}  {safe_title}  下载完成  抽帧完成   上传完成")
        except Exception as e:
            table_two.update_one({'_id':_id},{'$set':{"step":error_step,'error_reason':"下载过程出错"+str(e)}})



def check_video(item):
    pass

def upload_video(item):
    pass


curent_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if __name__ == '__main__':
    try:
        # add_count=into_db()
        # if add_count==0:
        #     raise ValueError(f"没有成功爬取到视频信息 by_uid 结果为 add_count  {add_count}")
        # logger.success(f"{curent_time}  爬取陈工  {add_count} 条入库")


        download_video()

    except Exception as e:
        tell_to_wx(str(e))
    


    




            
         

          