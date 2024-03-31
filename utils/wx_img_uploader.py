import json
import os
import time
from loguru import logger
from pymongo import MongoClient
import redis
import requests

weixin_gongzhonghao_appid = "wx80856473850271f3"
weixin_gongzhonghao_appsecret = "4058a18b3af06d026cc4704e445d4bd3"

import httpx
def get_request(url, proxies=None, retries=3,use_proxy=True,**kargs):
    exception = None
    for i in range(retries):
        try:
            if use_proxy:
                proxies=get_proxy_china_http()
            response = httpx.get(url, proxies=proxies,timeout=12,**kargs)
            response.raise_for_status()  # 如果响应状态码不是 200，就抛出异常
            return response
        except Exception as e:
            exception = e
    logger.error(f'Final attempt failed with error: {exception}')
    return None

class aio_save_media_by_wx():
    now_time = time.time()
    now_acess_token = ""

    # 获取一个新的 access_token
    def _get_new(self):
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={weixin_gongzhonghao_appid}&secret={weixin_gongzhonghao_appsecret}"
        data = get_request(url,use_proxy=False)
        access_token=""
        try:
            access_token=data.json()["access_token"]
        except Exception as e:
            logger.error(f'获取access_token失败: {e} {data.json()}')

        return access_token

    def get_acessToken(self):
        flag = (time.time() - self.now_time) // 3600 > 2
        if flag or self.now_acess_token == "":
            self.now_acess_token =  self._get_new()
            logger.info("get new acessToken")
        return self.now_acess_token

    def _sav_to_local(self,  content):
        filename = f"./temp/{int(time.time()*100000)}.jpg"
        with open(filename, "wb") as ff:
            ff.write(content)
        return filename

    def _upload_media_to_wx_https(self, https_pic_url):
        pic_binary = get_request(https_pic_url)
        if not(pic_binary):
            return "",False

        filepath= self._sav_to_local(pic_binary.content)
        params = {"access_token": self.now_acess_token}

        with open(filepath, "rb") as ff:
            url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.now_acess_token}"
            try:
                response = httpx.post(url,params=params, files={"media": ff})
                data = response.json()
                text = response.text

                if "daily" in text:
                    logger.error('今日已经到达额度')
                    os._exit(0)

                media_id = data["media_id"]
                url = data["url"]
            except Exception:
                media_id = "error"
                url = False
                self.get_acessToken()
            finally:
                ff.close()
                os.remove(filepath)
                return media_id, url

    def _upload_local_media_to_wx_https(self, filepath):
            for ii in range(3):
                params = {"access_token": self.now_acess_token}
                with open(filepath, "rb") as ff:
                    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.now_acess_token}"
                    try:
                        response = httpx.post(url,params=params, files={"media": ff})
                        data = response.json()
                        text = response.text

                        if "daily" in text:
                            logger.error('今日已经到达额度')
                            os._exit(0)

                        media_id = data["media_id"]
                        url = data["url"]
                        return media_id, url
                    except Exception as e:
                        media_id = "error"
                        url = False
                        self.get_acessToken()
                    finally:
                        ff.close()
            raise ValueError("上传异常 ")


if __name__ == '__main__':
    wx_gzh=aio_save_media_by_wx()
    data=wx_gzh._upload_local_media_to_wx_https(r"C:\projects\py_win\spider_up_topic\assert\大型纪录片\我只不过是有点视觉疲劳了_而他们却是真的失去了至亲_\extracted_frames\frame_3.jpg")
    print(data)



