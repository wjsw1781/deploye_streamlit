# -*- coding: utf-8 -*-
import re
import sys,os
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







import hashlib
import os
import time
from bilibili_api import Credential
import httpx
from loguru import logger
import moviepy.editor as mp
import requests
cookies = {
    'buvid3': 'F962C52E-1A98-243D-7D97-4CCBE2966F0326637infoc',
    'b_nut': '1711818926',
    'i-wanna-go-back': '-1',
    'b_ut': '7',
    'b_lsid': 'E385FEB5_18E905BE99B',
    'bsource': 'search_baidu',
    '_uuid': 'F101ECB57-AE93-79810-A8FC-668FB3F28A9E26516infoc',
    'enable_web_push': 'DISABLE',
    'FEED_LIVE_VERSION': 'V_HEADER_LIVE_NO_POP',
    'header_theme_version': 'undefined',
    'home_feed_column': '4',
    'browser_resolution': '1044-1314',
    'buvid4': '2F77A97F-A871-F57E-554F-8835BB72B8D628834-024033017-dUPAC4eUHoBN8ubm2FnGbytKnBfoGDNJ1XWjUSvJ8OcGDDH4ObwKOgotCksXSOiX',
    'buvid_fp': 'bc037d32654f6edba6ddcaed6f61eab0',
    'SESSDATA': '62ce526a%2C1727370955%2C773ad%2A31CjAu1t684fEQ3u8qr-eQpF9H9jVjItu1UWwAXeFlkdFY0BCW3QprNFco7IXCPg3AO40SVkVCRGN5SElTMERCTHdrUGdfclFyeW9DSFVpQnhRQlJUNE84ZTFqakNvSDRpUlkwTlp5N0JUTGs5SnczRzlwNWxsaFR6Mk1BQkJURG5CYTBLVnJlSE5BIIEC',
    'bili_jct': '2376845b83742873f25953ad3f6577d2',
    'DedeUserID': '102742156',
    'DedeUserID__ckMd5': '68d517f8697ef166',
    'sid': 'dfawlj6d',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTIwNzgxNjMsImlhdCI6MTcxMTgxODkwMywicGx0IjotMX0.pUjz9Vyc_FInLcmbHTFJLvQRO_W_tIHbc4Nq6B4mF7s',
    'bili_ticket_expires': '1712078103',
    'PVID': '1',
}
credential = Credential.from_cookies(cookies)

from bilibili_api import video, sync, user, comment, session, HEADERS
from PIL import Image

FFMPEG_PATH = os.path.abspath(f'{project_dir}/ffmpeg.exe')


async def download_url(url: str, out: str, info: str):
    # 下载函数
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                process += len(chunk)
                f.write(chunk)


def download_url_big(url: str, out: str, info: str):
    # 下载函数
    with requests.get(url, stream=True, headers=HEADERS) as resp:
        resp.raise_for_status()
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_content(chunk_size=1024):
                if not chunk:
                    break
                process += len(chunk)
                f.write(chunk)

# 获取所有视频
async def get_all_videos(she, end_pn=10):
    init = list(range(1, end_pn + 1))
    all_videos = []
    max_try=10
    cur_try=0
    # 如果失败了就重试
    for index, pn in enumerate(init):
        try:
            videos = await she.get_videos(0, pn, 30)
        except Exception as e:
            videos = []
            logger.error(f"{index} /{len(init)} {e} -----> 页获取失败 直接记录了")
            time.sleep(10)
            init.append(pn)
            cur_try+=1
            if cur_try>max_try:
                logger.error(f"{index} /{len(init)} 重试次数过多 退出")
                break
            continue
            continue
        videos_meta = videos['list']['vlist']
        all_videos += videos_meta
        logger.debug(f"{pn}  -----> {len(all_videos)}   获取陈工")
        time.sleep(5)
    return all_videos


# 获取视频播放链接--->提取音频
async def download_video_best(bvid, aid, local_filename):
    video_ele = video.Video(bvid=bvid, aid=aid, credential=credential)
    video_info = await video_ele.get_download_url(page_index=0)
    detecter = video.VideoDownloadURLDataDetecter(data=video_info)
    streams = detecter.detect_best_streams()
    if detecter.check_flv_stream() == True:
        flv_name = local_filename + ".flv"
        await download_url(streams[0].url, flv_name, "FLV 音视频流")
        os.system(f'{FFMPEG_PATH} -i {flv_name} {local_filename}')
        os.remove(flv_name)

    else:
        video_temp = local_filename + "video_temp.m4s"
        audio_temp = local_filename + "audio_temp.m4s"
        await download_url(streams[0].url, video_temp, "视频流")
        await download_url(streams[1].url, audio_temp, "音频流")

        os.system(f'{FFMPEG_PATH} -i {video_temp} -i {audio_temp} -vcodec copy  -acodec copy {local_filename} -y')
        os.remove(audio_temp)
        os.remove(video_temp)

# 裁剪 以及缩放
def scale_and_crop_video(video_path, scaled_video_path, size_rate=1.2, watermark_text="永远热爱"):
    # 从中心出发 获取原本的宽高就是裁切啊
    video = mp.VideoFileClip(video_path)
    scaled_video = video.fx(mp.vfx.resize, size_rate)
    scaled_video = scaled_video.crop(x_center=scaled_video.w / 2, y_center=scaled_video.h / 2, width=video.w,
                                     height=video.h)

    # 添加文本水印
    txt_clip = (mp.TextClip(watermark_text, fontsize=24, color='white', print_cmd=True)
                .set_position((45,120))
                .set_duration(scaled_video.duration)
                .set_opacity(0.5))
    scaled_video = mp.CompositeVideoClip([scaled_video, txt_clip])

    scaled_video.write_videofile(scaled_video_path, threads=10)

    video.close()
    return scaled_video_path


# 获取视频html5可在线观看
def preview_h5_video_url(bvid, aid):
    html5_url=f'http://player.bilibili.com/player.html?aid={aid}&bvid={bvid}'
    return html5_url

# 获取视频某一帧画面
from moviepy.editor import VideoFileClip
import os

def extract_four_frames(video_path):
    all_img_path = []
    # Load the video clip
    clip = VideoFileClip(video_path)
    
    # Get the duration of the video
    duration = clip.duration
    
    # Define the time points for the four frames
    frame_times = [duration * (i + 0.5) / 4 for i in range(4)]
    
    # Create a directory to save the frames
    dir_name=os.path.dirname(video_path)
    frames_dir = f'{dir_name}/extracted_frames'
    os.makedirs(frames_dir, exist_ok=True)
    
    # Extract frames at the specified time points
    for i, time in enumerate(frame_times):
        # Set the frame to be extracted at the specified time point
        frame = clip.get_frame(time)
        
        # Save the frame as an image file
        image = Image.fromarray(frame)
            
        # Save the image as a JPEG file
        frame_path = os.path.join(frames_dir, f'frame_{i}.jpg')
        image.save(frame_path)
        all_img_path.append(frame_path)
    # Close the video clip
    clip.close()
    
    return all_img_path

# 同步获取视频列表 /////////////////////
def get_all_videos_sync(uid, end_pn=3):
    she = user.User(uid, credential=credential)
    all_videos = sync(get_all_videos(she, end_pn))
    return all_videos


def download_video_sync(bvid, aid, filename):
    try:
        video_info = sync(download_video_best(bvid, aid, filename))
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    # uid=27547211
    # all_videos=get_all_videos_sync(uid)
    # logger.success(f'获取视频成功    ---->   {all_videos}  ')

    aid=1051375894
    bvid='BV1UW421c7zm'
    filename='./test.mp4'

    # video_info=download_video_sync(bvid,aid,filename)
    # logger.success(f'下载视频成功    ---->   {video_info}  ')

    # last_mp4 = r"C:\projects\zhiqiang_hot\video.mp4"
    # video_scaled_last_mp4 = r"C:\projects\zhiqiang_hot\video_scaled.mp4"
    # scale_and_crop_video(last_mp4, video_scaled_last_mp4, 1.2)


    # h5_url=sync(preview_h5_video_url(bvid, aid))
    # print("🚀 ~ h5_url:", h5_url)

    h5_url=extract_four_frames(filename)
    print("🚀 ~ h5_url:", h5_url)

"""
<iframe src="//player.bilibili.com/player.html?aid=1051375894&bvid=BV1sH4y1j7uX&cid=1461245640&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>


"""