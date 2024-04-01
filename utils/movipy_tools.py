import os


when_import_the_module_the_path=os.path.dirname(__file__)








import random
import subprocess
import time
from loguru import logger
from moviepy.editor import VideoFileClip

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.config import get_setting
from moviepy.tools import subprocess_call

def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Execution time of {func.__name__}: {execution_time} seconds")
        return result
    return wrapper

@measure_execution_time
def crop_video_top_ratio(video_path, output_path, crop_height_ratio):
   
    # Get video dimensions
    clip = VideoFileClip(video_path)
    width = clip.size[0]
    height = clip.size[1]

    crop_height = int(height * crop_height_ratio)
    still_height = height - crop_height
    start_point = (0, crop_height)
    watermark_path=f"{when_import_the_module_the_path}/watermark.png"
    shuiyin_position=random.choice(['W-w-10:H-h-10','W-w-10:(H-h-10)/2','W-w-10:0',])
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", watermark_path,
        "-filter_complex",
        f"[0:v][1:v]overlay={shuiyin_position},crop={width}:{still_height}:{start_point[0]}:{start_point[1]}", 
        output_path,
        '-y'
    ]
    subprocess_call(cmd)
    # subprocess_call_python(cmd)

    return True

@measure_execution_time
def crop_video_s_start(video_path, output_path, s_start):
   
    clip = VideoFileClip(video_path)
    duration = clip.duration
    
    cmd = [
        "ffmpeg",
        "-ss", str(s_start),
        "-i", video_path,
        "-t", str(duration - s_start), 
        "-c:v", "copy",
        "-c:a", "copy",
        output_path,
        '-y'
    ]
    subprocess_call(cmd)
    return True




if __name__ == '__main__':

    video = r"D:\projects\deploy_streamlit\spider_up_topic\assert\大型纪录片\_当年军师满眼泪花_才让现在的你步步绝杀__\video.mp4"
    output = video+"_crop.mp4"
    crop_height_ratio=0.09

    crop_video_top_ratio(video, output, crop_height_ratio)
    outputss = video+"_ss.mp4"
    s_start=5
    crop_video_s_start(video, outputss, s_start)
