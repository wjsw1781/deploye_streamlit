
# -*- coding: utf-8 -*-
import sys,os
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)
sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(os.path.dirname(os.path.dirname(parent_dir)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(parent_dir))))
sys.path.append(basedir)





from pymongo import MongoClient

table_name='yu_gao_pian'
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot
table=db[table_name]


from huanjie_zhuangtai import Stage,pipeline

ther_piplie=pipeline(name="预告片处理流程")

ther_piplie.add_stage(Stage('web_ui_choose_bvid_init'))
ther_piplie.add_stage(Stage('下载本地'))
ther_piplie.add_stage(Stage('移除水印和时间轴'))
ther_piplie.add_stage(Stage('抖音投稿'))
ther_piplie.add_stage(Stage('视频号投稿'))
ther_piplie.add_stage(Stage('快手投稿'))


item={
    'pipeline':ther_piplie.output_pipeline(),
}


def init_config_to_all():
    global item
    table.update_many({},{"$set":item})

    print('重置状态成功',)
    for ii in ther_piplie.pipeline:
        print(ii)



def init_one(_id):
    global item
    table.update_one({"_id":_id},{"$set":item})
    print('重置状态成功',_id)



# 添加流程  实在是ui无法进行添加这个操作 只能在这里进行了

if __name__ == '__main__':

    init_config_to_all()


   























