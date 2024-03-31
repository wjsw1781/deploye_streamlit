# encoding=utf-8
import m3u8
import requests
import datetime
import os
from Crypto.Cipher import AES
from Crypto import Random
import glob
# Request header, not necessary, see website change
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
"""
 pip install pycryptodome  -i https://pypi.tuna.tsinghua.edu.cn/simple 

"""

 
 
def download(ts_urls, download_path, keys=[]):
    if not os.path.exists(download_path):
        os.mkdir(download_path)
 
    decrypt = True
    if len(keys )== 0 :  # m3u8 will get [None] if not key or []
        decrypt = False
 
    for i in range(len(ts_urls)):
        ts_url = ts_urls[i]
        file_name = 'https://v4-vod.kwaicdn.com/ksc2/'+ts_url.uri
        print("start download %s" %file_name)
        start = datetime.datetime.now().replace(microsecond=0)
        try:
            response = requests.get(file_name, stream=True, verify=False)
        except Exception as e:
            print(e)
            raise ValueError('某个片段失败')
         
 
        ts_path = download_path+"/{0}.ts".format(i)
        if decrypt:
            key = keys[i]
            iv = Random.new().read(AES.block_size)
            cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC)
 
        with open(ts_path,"wb+") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    if decrypt:
                        file.write(cryptor.decrypt(chunk))
                    else:
                        file.write(chunk)
 
        end = datetime.datetime.now().replace(microsecond=0)
        print("total time：%s"%(end-start))
 
def merge_to_mp4(dest_file, source_path, delete=True):
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    with open(dest_file, 'wb') as fw:
        files = glob.glob(source_path + '/*.ts')
        for file in files:
            with open(file, 'rb') as fr:
                fw.write(fr.read())
                print(f'\r{file} Merged! Total:{len(files)}', end="     ")
            os.remove(file)
 
def m3u8_to_mp4(m3u8_url, output_file, decrypt=False, keys=None):
    m3u8_file='./key.m3u8'
    with open(m3u8_file, 'wb') as ff:
        ff.write(requests.get(m3u8_url).content)
    video = m3u8.load(m3u8_file)
    download(video.segments, 'tmp', [])
    merge_to_mp4(output_file, 'tmp')
    pass


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









if __name__ == "__main__":
    url = "https://v4-vod.kwaicdn.com/ksc2/a7IPRdpwwpT4cuTdTC33aSY0ClR0MOfdlCyJm-OJT9IldEPjbl7XruOyDfbUIJdjxRINYMZCNfWUYRcFx_r52Q.m3u8?pkey=AAVffduyGsJvEXURqDixwTWB195wc_UjhnTsgyJvBUQkWBDQbBqNvP-FwY9vQ2-GFd5Ao_vLGobwVTEuR_rx5OdQ3WwuEv_pzhQ0fTaUbNuDAncLrHwNVdQHs7TO6C02pTQ&ss=vp"
    m3u8_file='./key.m3u8'
    with open(m3u8_file, 'wb') as ff:
        ff.write(requests.get(url).content)
    video = m3u8.load(m3u8_file)
    print(video.data)
    download(video.segments, 'tmp', [])
    merge_to_mp4('result.mp4', 'tmp')