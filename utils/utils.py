import glob
import hashlib
import os
import time
import httpx
from loguru import logger

def md5(string):
    string=str(string)
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Range': 'bytes=0-',
    'Referer': 'https://v1.kwaicdn.com/ksc1/goB-_3z9CelYBxBxsWKhbuKlli8vUFI5ee0EcXRHhaDOZL02XmNlgqqv2CdxMPIUl-T2TrUVj-xXOOBoEFSHZt9K4Z76KPYFb8pFtaVGZBn48Y4m6vqACF5ho7KBNzC19BXJACPiePNQvcWjX7OlVfbcvas3y8bKiaOankeJ8N67jL_ngGQygamj6D7kYSWU.mp4?pkey=AAUhRh938uCf2KMoZuwquYTzRz3JsmDJSO0o3kcqE0Sg3AWwqpO-3elNPggF0ds-JBxU1pw3TdRhctLsXqSMBKQzOQyz447z31PV2LVVuYuVSTBE_wxwwGE8XgsE09TO2Zw&tag=1-1710663052-tube-0-es2vxka9fh-1f61bc325a16dd0c&clientCacheKey=3xjkkuarq23eiu6_b.mp4&v=ec3yz9a08b282&bp=14081',
    'Sec-Fetch-Dest': 'video',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


async def download_url_big_file(url: str, out: str, info: str):
    # 下载函数
    async with httpx.AsyncClient(headers=headers) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                process += len(chunk)
                f.write(chunk)
                logger.info(f"{info} 下载进度: {process}/{length}")
        return True
    

import requests

def download_url_big_file_sync(url: str, out: str, info=""):
    # 下载函数
    with requests.get(url, stream=True) as resp:
        resp.raise_for_status()
        length = int(resp.headers.get('content-length'))
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_content(chunk_size=1024):
                if not chunk:
                    break
                process += len(chunk)
                f.write(chunk)

                if process%3024000==0:
                    logger.info(f"{info} 下载进度: {process}/{length}  {process/length*100:.2f}")
        return True


def get_safe_title(title):
    import re
    if not title:
        return ''
    legal_characters = re.compile(r'[^a-z0-9\u4E00-\u9FA5]', re.IGNORECASE)
    safe_title = legal_characters.sub('_', title)
    return safe_title

from .img_handler import generate_transparent_image,image_add_text,generate_horizontal_process_flow



def merge_to_mp4(dest_file, source_path, delete=True):
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    with open(dest_file, 'wb') as fw:
        files = glob.glob(source_path + '/*.ts')
        for file in files:
            with open(file, 'rb') as fr:
                fw.write(fr.read())
                # print(f'\r{file} Merged! Total:{len(files)}', end="     ")
            os.remove(file)
 
from .bilibili import preview_h5_video_url,search_topic_by_kw_sync,download_video_sync,extract_four_frames,bili_get_up_videos_sync


def tell_to_wx(info):
    import requests
    data={
    'msgtype': 'text',
    'text': {
        'content': info,

    }
    }

    url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4ff43b98-5254-47ee-844d-471b52f6dd56'
    requests.post(url=url,json=data)



from .wx_img_uploader import aio_save_media_by_wx

def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Execution time of {func.__name__}: {execution_time} seconds")
        return result
    return wrapper

# 视频剪辑
from .movipy_tools import crop_video_s_start,crop_video_top_ratio,only_fix_audio



from .chrome_window import get_one_window_with_out_proxy



from lxml import etree

from urllib.parse import urljoin


def html_to_lxml(html_string):
    return etree.HTML(html_string)


def html_to_string(html):
    return etree.tostring(html, encoding='utf-8').decode()


def extract_img_url(img_tag):
    urls = []
    for attr, value in img_tag.items():
        if value.startswith(('http', '/')) or '/' in value:
            urls.append(value)
    if len(set(urls)) >= 1:
        return urls[0]
    return ''


def format_img_src(html: str, base_url) -> str:
    ele = html_to_lxml(html)
    for img in ele.xpath('.//img'):
        try:
            src = extract_img_url(img)
            if 'base64' in src:
                continue
            img_url_full = urljoin(base_url, src)
            img.set('src', img_url_full)

        except Exception as e:
            continue
    abs_img_html = html_to_string(ele)
    return abs_img_html


def format_absolute_url(html:str,base_url) -> str:
    ele=html_to_lxml(html)
    for link in ele.xpath('.//a'):
        if 'href' in link.attrib:
            try:
                link_url_full = urljoin(base_url, link.attrib['href'])
                link.set('href', link_url_full)
            except Exception as e:
                continue
    abs_html = html_to_string(ele)
    abs_html = format_img_src(abs_html,base_url)
    return abs_html


def remove_element_safely(element):
    # 安全移除一个ele  lxml直接 parent.remove(element) 会导致 ele后面的文本会被删除 类似<img></img>aaa  aaa会被认为属于img
    parent = element.getparent()
    new_text_node = etree.Element('span')
    new_text_node.text = element.tail or ''
    parent.insert(parent.index(element), new_text_node)
    parent.remove(element)

def get_a_name_href(a):
    text=''.join(a.xpath('.//text()'))
    href=a.attrib['href']
    return text,href


def get_current_time():
    import datetime
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def retry(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Attempt {attempts + 1} failed:", e)
                    attempts += 1
                    time.sleep(delay)
            return False
        return wrapper
    return decorator