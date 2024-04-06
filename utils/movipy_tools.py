import os


when_import_the_module_the_path=os.path.dirname(__file__)



from PIL import Image, ImageDraw, ImageFont

def generate_transparent_image(text, font_size,output_image_path):
                               
    font_path=f'{when_import_the_module_the_path}/瘦金体.ttf'
    font = ImageFont.truetype(font_path, font_size)
    text_color=(255, 255, 255)
    background_color=(255, 255, 255, 0)
    image_width=len(text)*font_size+10

    img = Image.new("RGBA", (image_width, font_size + 10), background_color)
    draw = ImageDraw.Draw(img)

    draw.text((0,0), text,fill=text_color, font=font) # 设置水印位置
    img.save(output_image_path)

    return img





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
    if not os.path.exists(watermark_path):
        generate_transparent_image("永远热爱", 20,watermark_path)

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



from moviepy.editor import VideoFileClip, ImageClip
import os
from moviepy.editor import *


from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips



def one_img_2_video(img_path,width,height,duration=5,big_duration=10):
    img_2_video_path=os.path.abspath('./img_2_video_path.mp4')
    image = Image.open(img_path)
    original_width, original_height = image.size
    new_image = Image.new("RGB", (width, height ), color=(0, 0, 0))
    if original_width < width or original_height < height:
        scale = min(width / original_width, height / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        image = image.resize((new_width, new_height))
        paste_x = (width - new_width) // 2
        paste_y = (height - new_height) // 2
    else:
        new_width = original_width
        new_height = original_height
        paste_x = (width - original_width) // 2
        paste_y = (height - original_height) // 2
    new_image = Image.new("RGB", (width, height), color=(0, 0, 0))
    new_image.paste(image, (paste_x, paste_y))
    temp_img=img_path+"temp.png"
    new_image.save(temp_img)
    fps=30
    clip = ImageSequenceClip([temp_img]*fps*duration, fps = fps) 
    clip.write_videofile(img_2_video_path, fps=fps)
    return img_2_video_path


@measure_execution_time
def only_fix_audio(video_path, output_path):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-c:v", "copy",  # 复制视频流
        "-c:a", "aac",   # 使用 AAC 编码音频
        "-strict", "-2", # 确保兼容性
        output_path,
        '-y'             # 覆盖目标文件（如果存在）
    ]
    subprocess_call(cmd)
    return True


@measure_execution_time
def add_image_to_video_start(image_path, video_path, output_path,duration=5):
    # 检查图片和视频路径是否存在
    if not os.path.exists(image_path):
        print("Error: 图片路径不存在")
        return False
    if not os.path.exists(video_path):
        print("Error: 视频路径不存在")
        return False

    video2 = VideoFileClip(video_path)
    width, height = video2.size
    img_2_video_path=one_img_2_video(image_path,width,height,duration,video2.duration)

    cmd=f'ffmpeg -i {img_2_video_path} -i {video_path} -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[outv]" -map "[outv]" -strict -2 {output_path}'
    os.system(cmd)

    # with open(output_path,'wb') as ff:
    #     with open(img_2_video_path,'rb') as f:
    #         ff.write(f.read())
    #     with open(video_path,'rb') as f:
    #         ff.write(f.read())
    # return True
    
            
# pic=r'C:\projects\deploy_streamlit\utils\龙珠封面.png'

# video='C:/projects/py_win/assert/龙珠/9fd01d2a118535035bd77af493641015/_16__.mp4'

# output='C:\projects\deploy_streamlit\output_video.mkv'

# add_image_to_video_start(pic,video,output)

if __name__ == '__main__':

    video = r"D:\projects\deploy_streamlit\spider_up_topic\assert\大型纪录片\_当年军师满眼泪花_才让现在的你步步绝杀__\video.mp4"
    output = video+"_crop.mp4"
    crop_height_ratio=0.09

    crop_video_top_ratio(video, output, crop_height_ratio)
    outputss = video+"_ss.mp4"
    s_start=5
    crop_video_s_start(video, outputss, s_start)
