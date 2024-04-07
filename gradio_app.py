# -*- coding: utf-8 -*-
import io
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
import functools
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot

# 查看  修改 两个功能
# 获取所有mongo的表名


all_table_names=db.list_collection_names()
page_size=10
pipeline_filed='pipeline'


# @functools.lru_cache(maxsize=128)
def get_mongo_skip_page(table_name,pagging):
    skip_page=pagging*page_size
    # 添加order属性
    logger.success(f'未命中缓存{table_name}   {pagging}')
    datalist=list(db[table_name].find({}).skip(skip_page).limit(page_size).sort("update_tm", -1))
    return datalist

def get_pinyin(text):
    from pypinyin import pinyin, Style
    pinyin_list = pinyin(text,style=Style.NORMAL)
    return '_'.join([p[0] for p in pinyin_list])

# 过滤掉df1中那些df2中已经存在的数据
def filter_after_in(df1,df2,filed='bvid'):
    # 两者都有的
    merged_df = pd.merge(df1, df2, on=filed, how='inner')

    # 获取需要过滤掉的索引信息
    filter_indices = merged_df.index

    # 过滤掉取反
    filtered_df_list_video = df1[~df1.index.isin(filter_indices)]

    return filtered_df_list_video


# 图片展示
from PIL import Image

from PIL import Image, ImageDraw

import functools



@functools.lru_cache()
def get_wx_img(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return image

def draw_line_on_image(url, slider_value_rate=0.5):
    if slider_value_rate=="":
        slider_value_rate=0.5
    image=get_wx_img(url)
    width, height = image.size
    
    slider_value_rate_y=int(height*slider_value_rate)

    line_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(line_image)
    draw.line([(0, slider_value_rate_y), (width, slider_value_rate_y)], fill="red", width=3)
    combined_image = Image.blend(image, line_image, alpha=0.5)
    return combined_image


with gr.Blocks(fill_height=True,) as demo:

    with gr.Tab(label='大型纪录片的设计-一切从topic开始'):
        all_topic=list(db['topic'].find({}))
        topic_df=pd.DataFrame(all_topic)

        with gr.Row():
            # gr 提醒
            info=gr.Warning()

        with gr.Row():
            group=gr.Dropdown(choices=topic_df['group'].to_list(),label='选择一个分组')
            topic=gr.Dropdown(choices=topic_df[topic_df['group']==group.value]['topic'].to_list(),label='选择一个子组')
            key_word=gr.Textbox(label='输入关键词',value='',placeholder='默认是group和subgroup的拼接')
            search_btn=gr.Button(value='搜索')

        with gr.Row(equal_height=True):
            search_html=gr.HTML("",label='b站检索结果',)
            search_bvids_df=gr.Dataframe(label='检索到的bvid',height=700,scale=1)
            with gr.Column():
                current_item=gr.JSON(value={},label='一个json表示当前选中的条目',scale=1)
                add_in_db=gr.Button(value='入库',elem_id='add_in_db')

        with gr.Row():
            pre_one_item=gr.HTML("",label='预览一个后台请求到视频')

        with gr.Row():
            have_in_db=gr.Dataframe(label='当前已入库的数据',height=1000)
            with gr.Column():
                shuiyin_positon=gr.Slider(interactive=True,label='水印区域',minimum=0.0,maximum=100.0,step=1.0,value=0)
                shijianzhou_part=gr.Slider(interactive=True,label='时间轴区域',minimum=0.0,maximum=100.0,step=1.0,value=0)
                with gr.Row():
                    ok_btn=gr.Button(value='批量修改水印上百分比|时间轴绝对位置',interactive=True)
                    error_btn=gr.Button(value='这个不行',interactive=True)

                with gr.Column():
                    img1=gr.Image()
                    img2=gr.Image()
                    img3=gr.Image()
                    img4=gr.Image()


        # 意味着选择表  改动两个部分
        @group.change(inputs=group, outputs= [topic,have_in_db])
        def update_sub_group_topic(group):
            sub_topic=topic_df[topic_df['group']==group]['topic'].to_list()
            topic=gr.Dropdown(choices=sub_topic,label='选择一个子组')
            table_name=get_pinyin(group)

            all_table_item=[]
            for ii in range(100):
                page_items=get_mongo_skip_page(table_name,ii)
                if len(page_items)==0:
                    break
                all_table_item.extend(page_items)
            gr.Warning(f'加载到 {ii} 页内容 ') 
            #那个group下的所有数据
            have_in_db_value_df=pd.DataFrame(all_table_item)

            return [topic,have_in_db_value_df]

        @topic.change(inputs=[group,topic], outputs= [key_word])
        def update_key_word(group,topic):
            key_word=f"{group}-{topic}"
            return key_word
        
        @search_btn.click(inputs=[key_word,have_in_db], outputs= [search_html,search_bvids_df])
        def search_bvids_by_key_word(key_word,have_in_db):
            url=f'https://search.bilibili.com/all?keyword={key_word}&from_source=webtop_search&spm_id_from=333.1007&search_source=5'
            search_html_value = f'<iframe src={url} width="100%" height="700px" frameborder="0" allow="autoplay"></iframe>'

            list_video=search_topic_by_kw_sync(key_word)
            df_list_video=pd.DataFrame(list_video)
            if len(have_in_db)==0 or len(df_list_video)==0:

                filter_df=df_list_video
            else:
                filter_df=filter_after_in(df_list_video,have_in_db)
            return [search_html_value,filter_df]
        
        @add_in_db.click(inputs=[group,topic,key_word,current_item],outputs=info)
        def scrapy_bvids_by_search_html(group,topic,key_word,current_item):
            table_name=get_pinyin(group)

            item={**current_item,'group':group,'topic':topic,'key_word':key_word,}
            item['update_tm']=get_current_time()
            title=item['title']
            _id=md5(item['bvid'])
            db[table_name].update_one({'_id':_id},{'$set':item},upsert=True)
            
            return gr.Warning(f'添加成功 {_id}  {title}') 
         
        
        @search_bvids_df.select(inputs=[search_bvids_df], outputs= [pre_one_item,current_item])
        def when_select(search_bvids,evt: gr.SelectData):
            current_item=search_bvids.iloc[evt.index[0]].to_dict()
            if "mid" in current_item and len(str(current_item['mid']))>5:
                mid=current_item['mid']
            else:
                mid=3493083962411195

            show_item={
                    "_id":md5(current_item['bvid']),
                    "id":current_item['id'],
                    "author":current_item['author'],
                    "arcurl":current_item['arcurl'],
                    "aid":current_item['aid'],
                    "bvid":current_item['bvid'],
                    "title":current_item['title'],
                    "description":current_item['description'],
                    "play":current_item['play'],
                    "tag":current_item['tag'],
                    "review":current_item['review'],
                    "pubdate":current_item['pubdate'],
                    "senddate":current_item['senddate'],
                    "duration":current_item['duration'],
            }
            bvid=current_item['bvid']
            pre_one_item_value=f'<iframe src="https://player.bilibili.com/player.html?bvid={bvid}" width="100%" height="700px" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>'
            return [pre_one_item_value,show_item]

        @shuiyin_positon.change(inputs=[shuiyin_positon,current_item], outputs= [img1,img2,img3,img4])
        def when_change_slider(shuiyin_positon,current_item):
            shuiyin_positon=shuiyin_positon/100

            img1=draw_line_on_image(current_item['four_wx_imgs'][0],shuiyin_positon)
            img2=draw_line_on_image(current_item['four_wx_imgs'][1],shuiyin_positon)
            img3=draw_line_on_image(current_item['four_wx_imgs'][2],shuiyin_positon)
            img4=draw_line_on_image(current_item['four_wx_imgs'][3],shuiyin_positon)
            return [img1,img2,img3,img4]
        
        @have_in_db.select(inputs=[have_in_db], outputs= [pre_one_item,current_item,shuiyin_positon,img1,img2,img3,img4])
        def when_select(have_in_db,evt: gr.SelectData):
            current_item=have_in_db.iloc[evt.index[0]].to_dict()
            if "mid" in current_item and len(str(current_item['mid']))>5:
                mid=current_item['mid']
            else:
                mid=3493083962411195

            shuiyin_positon_rate=current_item.get('shuiyin_positon_rate',0)
            four_wx_imgs=current_item.get('four_wx_imgs',[])
            if not(shuiyin_positon_rate):
                shuiyin_positon_rate=0
            if len(four_wx_imgs)!=4:
                four_wx_imgs=[
                    'https://picx.zhimg.com/v2-dd20355c2989cafa233cd1c840571877_l.jpg?source=32738c0c',
                    'https://picx.zhimg.com/v2-dd20355c2989cafa233cd1c840571877_l.jpg?source=32738c0c',
                    'https://picx.zhimg.com/v2-dd20355c2989cafa233cd1c840571877_l.jpg?source=32738c0c',
                    'https://picx.zhimg.com/v2-dd20355c2989cafa233cd1c840571877_l.jpg?source=32738c0c',
                              ]

            show_item={
                    "_id":current_item['_id'],
                    "id":current_item['id'],
                    "bvid":current_item['bvid'],
                    "title":current_item['title'],
                    "author":current_item['author'],
                    "play":current_item['play'],
                    "duration":current_item['duration'],
                    
                    "mid":mid,
                    "four_wx_imgs":four_wx_imgs,
                    "shuiyin_positon_rate":shuiyin_positon_rate,
                    **current_item,

            }
            if 'step' in current_item and current_item['step']==999:
                gr.Warning('这个已经被标记不能使用了  水印太大或者其他!!!')

            bvid=current_item['bvid']
            pre_one_item_value=f'<iframe src="https://player.bilibili.com/player.html?bvid={bvid}" width="100%" height="700px" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>'

            new_shuiyin_positon=gr.Slider(interactive=True,label='水印区域',minimum=0.0,maximum=100.0,step=1.0,value=shuiyin_positon_rate*100)


            img1=draw_line_on_image(four_wx_imgs[0],shuiyin_positon_rate)
            img2=draw_line_on_image(four_wx_imgs[1],shuiyin_positon_rate)
            img3=draw_line_on_image(four_wx_imgs[2],shuiyin_positon_rate)
            img4=draw_line_on_image(four_wx_imgs[3],shuiyin_positon_rate)
            return [pre_one_item_value,show_item,new_shuiyin_positon,img1,img2,img3,img4]

        @ok_btn.click(inputs=[shuiyin_positon,current_item,group], outputs=info)
        def when_click_ok_btn(shuiyin_positon,current_item,group):
            shuiyin_positon_rate=shuiyin_positon/100
            author=current_item['author']
            table_name=get_pinyin(group)
            db[table_name].update_many({'author':author},{'$set':{'shuiyin_positon_rate':shuiyin_positon_rate,}})
            return gr.Warning(f'{author} 的所有稿件已标注水印位置  {shuiyin_positon_rate} ') 

        @error_btn.click(inputs=[current_item,group], outputs=info)
        def when_click_ok_btn(current_item,group):
            table_name=get_pinyin(group)
            _id=current_item['_id']
            # 反馈这个为彻底不能用
            db[table_name].update_many({'_id':_id},{'$set':{'step':999,}})
            return gr.Warning(f'{_id} 不能用了 已标记为 step 999 ') 


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















