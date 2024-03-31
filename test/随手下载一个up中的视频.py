# -*- coding: utf-8 -*-
from datetime import timedelta
import sys, os
import time

from loguru import logger

basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)

sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(os.path.dirname(os.path.dirname(parent_dir)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(parent_dir))))

os.chdir(basedir)

print('basedir-------------->', basedir)
sys.path.append(basedir)

from utils import bilibili

logger.add('./logs/{time:YYYY-MM-DD}test.log', format='{time} {level} {message}', rotation=timedelta(days=1),
           retention=3)




if __name__ == '__main__':

    uids = [
        498421499, 546562340849750, 3546576924445007,
        3494376900659223,
        1068765283, 1701648043, 620314864, 3461563927235282,
        1524045459, 1628708018,

    ]

    for uid in uids:

        all_video = bilibili.get_all_videos_sync(uid, 1)

        good_video = list(filter(lambda x: x['play'] > 10000, all_video))
        for video in good_video:
            title = video['title']
            bvid = video['bvid']
            aid = video['aid']

            local_name = os.path.abspath(f'./assert/大型纪录片/{title}')
            pic_index = f"{local_name}/index.jpg"
            pic_index_url = video['pic']
            video_mp4_name = f"{local_name}/video.mp4"
            video_mp4_namegood = video_mp4_name + "good.mp4"
            os.makedirs(local_name, exist_ok=True)

            if os.path.exists(video_mp4_name):
                if os.path.exists(video_mp4_namegood):
                    continue

            import requests
            with open(pic_index, 'wb') as ff:
                ff.write(requests.get(pic_index_url).content)

            flag = bilibili.download_video_sync(bvid=bvid, aid=aid, filename=video_mp4_name)
            if not (flag):
                logger.error(f"下载失败---->  {video_mp4_name}")
                continue
            logger.success(f"下载陈工---->  {video_mp4_name}")
