# -*- coding: utf-8 -*-
import json
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
from utils.utils import *

client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot

# 查看  修改 两个功能
# 获取所有mongo的表名


all_table_names=db.list_collection_names()
page_size=30
pipeline_filed='pipeline'

def get_mongo_skip_page(table_name,pagging):
    # 获取跳过的条数
    skip_page=pagging*page_size
    datalist=list(db[table_name].find({}).skip(skip_page).limit(page_size))
    return datalist

with gr.Blocks(fill_height=True) as demo:
    def topic_table_choose():
        all_topic=list(db['topic'].find({}))
        
        df=pd.DataFrame(all_topic)
        return df

    with gr.Tab(label='大型纪录片的设计'):
        with gr.Row():
            # 下拉框
            gr.Dropdown(choices=all_table_names,label='选择想要操作的话题',show_label=False)
            pass
        with gr.Row():
            pass
        with gr.Row():
            pass

    with gr.Tab(label='新增话题'):
        pass
    


    with gr.Tab(label='龙珠开始的设计|查看功能为主'):
        with gr.Row():
            show_or_change=gr.Radio(label='选择关键视图', choices=['查看数据表', '修改数据表', ])

        with gr.Row():
            table_choice=gr.Radio(choices=all_table_names,show_label=False)
            pagging=gr.Slider(minimum=0,maximum=10,step=1,value=0,show_label=False,interactive=True)
            df_col_names=gr.CheckboxGroup(choices=['_id', 'title', 'step'],show_label=False,interactive=True)


        with gr.Row(equal_height=True):
            table_df=gr.Dataframe(pd.DataFrame([]),label="数据表",interactive=True,height=600)
            with gr.Column():
                detail_recorder=gr.TextArea(value={},label="详细的展示一条记录以及器状态",interactive=True)
                detail_recorder_json=gr.JSON(value={},label="详细的展示一条记录以及器状态")
            pip_pic=gr.Image()
            

        @table_choice.change(inputs=table_choice, outputs= [table_df,pagging,df_col_names])
        def update_table_df_by_table(table_choice):
            all_docs_num=db[table_choice].count_documents({})
            new_pagging=gr.Slider(minimum=0,maximum=all_docs_num//page_size,step=1,value=0,show_label=False,interactive=True)

            data_list=get_mongo_skip_page(table_choice,0)
            new_table_df=pd.DataFrame(data_list)

            colnums=new_table_df.columns.to_list()
            nwe_df_col_names=gr.CheckboxGroup(choices=colnums,value=['_id', 'title', 'step'],show_label=False,interactive=True)
            return (new_table_df,new_pagging,nwe_df_col_names)
        
        @pagging.change(inputs=[table_choice,pagging], outputs= table_df)
        def update_table_df_by_pagging(table_choice,pagging):
            data_list=get_mongo_skip_page(table_choice,pagging)
            new_table_df=pd.DataFrame(data_list)
            return new_table_df
        

        @df_col_names.input(inputs=[table_df,df_col_names], outputs= [table_df])
        def update_col_order(table_df:pd.DataFrame,df_col_names):
            reordered_cols = df_col_names + [col for col in table_df.columns if col not in df_col_names]
            new_df = table_df[reordered_cols]
            return new_df

        @table_df.select(inputs=[show_or_change,table_df], outputs= [detail_recorder,pip_pic])
        def when_select( show_or_change,table_df:pd.DataFrame,evt: gr.SelectData):
            try:
                value=table_df.iloc[evt.index[0]].to_dict()
                _id=value['_id']
            except Exception:
                return [None,None]

            if pipeline_filed in value and value[pipeline_filed]:
                pil_img=generate_horizontal_process_flow(json.loads(value[pipeline_filed]))
            else:
                pil_img=None    

            return [value,pil_img]
        @detail_recorder.change(inputs=[table_choice,show_or_change,detail_recorder], outputs= detail_recorder_json)
        def when_change(table_choice,show_or_change,detail_recorder):
            obj=eval(detail_recorder)
            if show_or_change=='修改数据表':
                _id=str(obj['_id'])
                db[table_choice].update_one({'_id':_id},{'$set':obj})
            return obj


    
demo.launch(server_port=8888, share=True,server_name='0.0.0.0')















