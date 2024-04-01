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







from pymongo import MongoClient

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
kind="大型纪录片"

item={
    'uid':498421499,
    'key':498421499,
    'up_name':"我是李四儿",
    '_id':md5(498421499),
}
table_one.update_one({'_id':item['_id']},{'$set':item},upsert=True)

# 入库 下载  抽帧  质检  投稿
# 入库0
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

# 0-2下载  抽帧  可以做到一起  没必要分开
def download_video():
    wx_gzh=aio_save_media_by_wx()

    from_step=video_item.is_spider_to_db
    end_step=video_item.is_up_4_pic_to_wx
    error_step=video_item.is_up_4_pic_to_wx+video_item.error_reason

    # table_two.update_many({'step':error_step},{'$set':{'step':from_step}})
    # table_two.update_many({'step':end_step},{'$set':{'step':from_step}})
    table_two.update_many({},{'$set':{'step':from_step}})

    for ii in table_two.find({'step':from_step}):
        try:
            _id=ii['_id']
            bvid=ii['bvid']
            aid=ii['aid']
            safe_title=ii['safe_title']
            local_name = os.path.abspath(f'./assert/{kind}/{safe_title}')
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
            if ii.get('all_wx_frame_pic_urls',[])==[] :
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
            else:
                all_wx_frame_pic_urls=ii['all_wx_frame_pic_urls']
            
            table_two.update_one({'_id':_id},{'$set':{
                "step":end_step,
                'all_wx_frame_pic_urls':all_wx_frame_pic_urls,
                                            }})
            logger.success(f"{curent_time}  {safe_title}  下载完成  抽帧完成   上传完成")
        except Exception as e:
            table_two.update_one({'_id':_id},{'$set':{"step":error_step,'error_reason':"下载过程出错"+str(e)}})

# 裁剪
def cut_video():
    # 人工认为成功 ---> 剪辑  投稿  ---->投稿成功  调用moviepy  调用chrome 比较麻烦 但也快结束了  马上结束
    from_step=video_item.is_human_ok
    end_step=video_item.is_tougao_success
    error_step=video_item.is_tougao_success+video_item.error_reason

    logger.success('裁剪开始')
    for ii in table_two.find({'step':{'$in':[from_step,error_step]}}):
        try:
            _id=ii['_id']
            safe_title=ii['safe_title']
            local_name = os.path.abspath(f'./assert/{kind}/{safe_title}')
            pic_index = f"{local_name}/index.jpg"
            video_mp4_name = f"{local_name}/video.mp4"
            video_mp4_namegood = video_mp4_name + "good.mp4"

            # 剪辑配置信息获取
            shijianzhou_delete_length=ii.get('shijianzhou_delete_length',0)
            shuiyin_bili=ii.get('shuiyin_bili',0.1)
            new_shijianzhou_delete_length=ii.get('new_shijianzhou_delete_length',None)
            new_shuiyin_bili=ii.get('new_shuiyin_bili',None)

            # 总是以用户侧观察的结果为准
            if new_shuiyin_bili is None:
                new_shuiyin_bili=shuiyin_bili
            if new_shijianzhou_delete_length is None:
                new_shijianzhou_delete_length=shijianzhou_delete_length
            video_mp4_namegood_temp=video_mp4_namegood+"temp.mp4"

            if not os.path.exists(video_mp4_namegood_temp):
                crop_video_top_ratio(video_mp4_name,video_mp4_namegood_temp,new_shuiyin_bili)
            
            if not os.path.exists(video_mp4_namegood):
                crop_video_s_start(video_mp4_namegood_temp,video_mp4_namegood,new_shijianzhou_delete_length)



            table_two.update_one({'_id':_id},{'$set':{"step":end_step,'video_mp4_namegood':video_mp4_namegood}})

            curent_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.success(f"{curent_time}  {safe_title}  裁剪 __-----__  完成")
        except Exception as e:
            logger.error(f"{curent_time}  {safe_title}  裁剪  出错")
            table_two.update_one({'_id':_id},{'$set':{"step":error_step,'error_reason':"裁剪 投稿过程中出错"+str(e)}})
    

    logger.success('裁剪完成\n\n')

if __name__ == '__main__':
    try:
        while 1:

        # add_count=into_db()
        # if add_count==0:
        #     raise ValueError(f"没有成功爬取到视频信息 by_uid 结果为 add_count  {add_count}")
        # logger.success(f"{curent_time}  爬取陈工  {add_count} 条入库")


        # download_video()
            cut_video()
            time.sleep(10)

    except Exception as e:
        tell_to_wx(str(e))
    


    




            
         

          