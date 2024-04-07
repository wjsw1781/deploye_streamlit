



# socks5://wzq:1213wzwz@8.218.62.26:55013

import time
import httpx


proxies = {
        'http://':'socks5://wzq:1213wzwz@8.218.62.26:55013',
        'https://':'socks5://wzq:1213wzwz@8.218.62.26:55013',
}


cookies = {
    '_ga': 'GA1.1.1152453097.1710770273',
    '__cred__': '',
    '__age_auth__': 'true',
    '_ga_RERSPC3P09': 'GS1.1.1712465923.2.1.1712467465.0.0.0',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    # 'cookie': '_ga=GA1.1.1152453097.1710770273; __cred__=; __age_auth__=true; _ga_RERSPC3P09=GS1.1.1712465923.2.1.1712467465.0.0.0',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}

params = {
    'isEnabledQuery': 'true',
    'searchText': '人生初   野々浦 暖',
    'isEnableAggregation': 'false',
    'release': 'false',
    'reservation': 'false',
    'soldOut': 'false',
    'from': '0',
    'aggregationTermsSize': '0',
    'size': '20',
}
from loguru import logger
while 1:
    time.sleep(30)
    try:
        response = httpx.get('https://www.prestige-av.com/api/search', params=params, cookies=cookies, headers=headers,proxies=proxies)
        res=len(response.json()['hits']['hits'])
        if res>3:
            logger.success("🚀🚀🚀🚀🚀get_num:",len(response.json()['hits']['hits']))
        logger.info(f" get_num:, {res}")
    except Exception as e:
        time.sleep(60*5)
    
# pip install httpx[socks] -i https://pypi.tuna.tsinghua.edu.cn/simple 
