# -*- coding: utf-8 -*-
import datetime
import statistics
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
from config import init_one,table

# 环节状态  这里只做一件事情就是发掘每个up主更多的视频  必须播放量要高于平均数


def main_logic(i):
    _id=i['_id']
    title=i['title']
    bvid=i['bvid']
    aid=i['aid']
    mid=i['mid']
    title=i['title']
    shuiyin_positon_rate=i.get('shuiyin_positon_rate',0.1)

    # 获取5页数据
    other_videos=bili_get_up_videos_sync(uid=mid,end_pn=20)
    # 计算平均数字播放量 还有中位数
    all_play=[]
    for j in other_videos:
        all_play.append(j['play'])
    median_value = statistics.median(all_play)
    mean_value = statistics.mean(all_play)
    magic_num=10000


    target_num=max(magic_num,mean_value,median_value)
    good_other_videos=[]
    for i in other_videos:
        if i['play']<=target_num:
            continue
        good_other_videos.append(i)
    
    for video in good_other_videos:
        video['_id']=md5(video['bvid'])
        video['find_by_other']=1
        video['shuiyin_positon_rate']=shuiyin_positon_rate

        table.update_one({'_id':video['_id']},{'$set':video},upsert=True)
        
    logger.success(f'{title}的作者 {mid} 挖掘完成  总共  {len(good_other_videos)}')
    return True
if __name__ == '__main__':

    while 1:
        # 暂时防止递归
        mids=[]

        try:
            cursor=table.find()
            for i in cursor:
                mid=i['mid']

                if mid in mids:
                    continue
                mids.append(mid)
            
                main_logic(i)

        except Exception as e:
            continue
        
        mids=[]
        logger.success(f'挖掘完成  ---->执行完成')
        time.sleep(1000)







            
         

          