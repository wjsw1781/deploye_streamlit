



class Vidoe_Item_Status:
    """
    Item状态
    # 爬取入库        
    # 下载本地
    # 抽帧到wx公众号
    # 人工质检通过
    # 投稿成功
    # 错误原因

    """
    is_spider_to_db = 0
    is_download_local = 1
    is_up_4_pic_to_wx = 2
    is_human_ok=3
    is_tougao_success=4
    error_reason=100

from pymongo import MongoClient


client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot

# 总共操纵两个表 一个所有发布这种视频的up主 id  一个是所有视频id
table_one=db['daxingjilupian_ups']
table_two=db['daxingjilupian_videos']
video_item=Vidoe_Item_Status()
kind="大型纪录片"
