
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

table_name='longzhuZ'
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot
table=db[table_name]



# 添加流程  实在是ui无法进行添加这个操作 只能在这里进行了

if __name__ == '__main__':
    from huanjie_zhuangtai import Stage,pipeline

    longzhu_pip_line=pipeline(name="龙珠处理流程")
    longzhu_pip_line.add_stage(Stage('下载本地'))
    longzhu_pip_line.add_stage(Stage('制作封面',step='ok'))
    longzhu_pip_line.add_stage(Stage('抖音投稿',step='ok'))
    longzhu_pip_line.add_stage(Stage('腾讯微视投稿'))

    item={
        'pipeline':longzhu_pip_line.output_pipeline(),
    }
    table.update_many({},{"$set":item})
    print('所有数据都已经成功重置状态如下')
    for ii in longzhu_pip_line.pipeline:
        print(ii)























