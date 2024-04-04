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

client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot

# 查看  修改 两个功能
# 获取所有mongo的表名


all_table_names=db.list_collection_names()
page_size=30

def get_mongo_skip_page(table_name,pagging):
    # 获取跳过的条数
    skip_page=pagging*page_size
    datalist=list(db[table_name].find({}).skip(skip_page).limit(page_size))
    return datalist

# 动态创建新的可输入组件到ui上
def dynamic_add_huanjie_zhuangtai(visible):
    with gr.Column(visible=visible) as one_huanjie:
    # 下拉框类型
        huanjie_zhuangtai=gr.Dropdown(choices=['制作封面', '视频裁切', '时间轴裁切', '音视频组装'],show_label=False,interactive=True)
        # 描述
        huanjie_zhuangtai_describe=gr.Textbox(placeholder='请输入描述',show_label=False,interactive=True)
        return one_huanjie

with gr.Blocks() as demo:
    # 选择关键视图  一些全局开关
    with gr.Row():
        show_or_change=gr.Radio(label='选择关键视图', choices=['查看数据表', '修改数据表', ])
        add_pipline_stage=gr.Button(value='增加pipline的环节', )

    with gr.Row():
        table_choice=gr.Radio(choices=all_table_names,show_label=False)
        pagging=gr.Slider(minimum=0,maximum=10,step=1,value=0,show_label=False,interactive=True)
        df_col_names=gr.CheckboxGroup(choices=['_id', 'title', 'step'],show_label=False,interactive=True)


    with gr.Row():
        table_df=gr.Dataframe(pd.DataFrame([]))
        detail_recorder=gr.Json(value={},label="详细的一条记录")

    # 动态添加处理流程到一个表里面的pipline字段上
    all_stage_zhanweifu=[]
    now_click=0
    with gr.Row():
        for i in range(10):
            one_stage = dynamic_add_huanjie_zhuangtai(visible=False)
            all_stage_zhanweifu.append(one_stage)


    @add_pipline_stage.click(inputs=None, outputs= [*all_stage_zhanweifu])
    def add_pipline_stage():
        new_all_stage_zhanweifu=[]
        global now_click
        for index,one_stage in enumerate(all_stage_zhanweifu):
            if index<=now_click:
                one_new_stage=dynamic_add_huanjie_zhuangtai(visible=True)
            else:
                one_new_stage=dynamic_add_huanjie_zhuangtai(visible=False)
            new_all_stage_zhanweifu.append(one_new_stage)
        now_click+=1
        return new_all_stage_zhanweifu

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
    def show_or_unshow_col(table_df:pd.DataFrame,df_col_names):
        reordered_cols = df_col_names + [col for col in table_df.columns if col not in df_col_names]
        new_df = table_df[reordered_cols]
        return new_df

    @table_df.select(inputs=[show_or_change,table_df], outputs= detail_recorder)
    def when_select( show_or_change,table_df:pd.DataFrame,evt: gr.SelectData):
        res={}
        if not evt.value:
            return res
        value=table_df.iloc[evt.index[0]].to_dict()
        if 'pipline' in value and value['pipline']:
            value['pipline']=json.loads(value['pipline'])

        res=value
        return res
    

demo.launch(server_port=8888, share=True,server_name='0.0.0.0')















