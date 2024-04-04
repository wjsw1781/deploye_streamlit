# -*- coding: utf-8 -*-
import sys,os

import pandas as pd
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)
when_import_the_module_the_path=os.path.dirname(__file__)

project_dir=basedir 
# 遍历所有父节点目录 如果存在readme.md文件 就返回那个目录
while True:
    if os.path.exists(os.path.join(project_dir, 'readme.md')):
        break
    project_dir = os.path.dirname(project_dir)
    if project_dir==os.path.dirname(project_dir):
        raise ValueError('未找到项目根目录')

sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(os.path.dirname(os.path.dirname(parent_dir)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(parent_dir))))

myenv=f'{project_dir}/myenv/Lib/site-packages/'
sys.path.append(myenv)


os.chdir(basedir)

print('basedir-------------->',basedir)
sys.path.append(basedir)


import gradio as gr
from pymongo import MongoClient

client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot

# 查看  修改 两个功能
# 获取所有mongo的表名


all_table_names=db.list_collection_names()
page_size=30

def get_mongo_skip_page(table_name,pagging):
    # 获取跳过的条数
    skip_page=pagging.value*page_size
    datalist=list(db[table_name].find({}).skip(skip_page).limit(page_size))
    return datalist


with gr.Blocks() as demo:
    # 选择关键视图
    with gr.Row():
        with gr.Column() as col1:
            show_or_change=gr.Radio(label='选择关键视图', choices=['查看数据表', '修改数据表', ])


    with gr.Row():
        table_choice=gr.Radio(choices=all_table_names,show_label=False)
        pagging=gr.Slider(minimum=0,maximum=10,step=1,value=0,show_label=False,interactive=True)


    with gr.Column():
        table_df=gr.Dataframe(pd.DataFrame([]))

    @table_choice.change(inputs=table_choice, outputs= [table_df,pagging])
    def update_table_df_by_table(table_choice):
        all_docs_num=db[table_choice].count_documents({})
        pagging.maximum=all_docs_num//page_size
        new_pagging=gr.Slider(minimum=0,maximum=pagging.maximum,step=1,value=0,show_label=False,interactive=True)

        data_list=get_mongo_skip_page(table_choice,pagging)
        new_table_df=pd.DataFrame(data_list)
        return (new_table_df,new_pagging)
    
    @pagging.change(inputs=pagging, outputs= [table_df])
    def update_table_df_by_pagging(pagging):
        data_list=get_mongo_skip_page(table_choice.value,pagging)
        new_table_df=pd.DataFrame(data_list)
        return (new_table_df)
    

    with gr.Column():
        pass
    with gr.Column():
        pass
    

demo.launch(server_port=8888, share=True)















