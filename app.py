
# -*- coding: utf-8 -*-
import re
import sys,os
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)

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

myenv=f"{project_dir}/myenv/Lib/site-packages/"
sys.path.append(myenv)


os.chdir(basedir)

print('basedir-------------->',basedir)
sys.path.append(basedir)






import functools
from io import BytesIO
import pandas as pd
import streamlit as st

from pymongo import MongoClient

from utils.utils import *
st.set_page_config(layout="wide")
st.title("增删改查mongo数据库  + 特定组件组合")


"""
几个状态变量
choose_table
page_number
page_size
data_df
selected_rows
video_info    包含水印  时间轴  完整描述

"""
st.session_state['choose_table']=None
st.session_state['page_number']=1
st.session_state['page_size']=30
st.session_state['data_df']=pd.DataFrame({})
st.session_state['selected_rows']=pd.DataFrame({})

# detail页需要的状态变量
st.session_state['video_info']={"shuiyin":[],"shijianzhou":[]}
st.session_state['shijianzhou_delete_length']=3
st.session_state['shuiyin_bili']=0.2
st.session_state['selected_values']=[0,1,2]


@st.cache_resource
def get_db():
    client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
    db = client.zhiqiang_hot
    return db
from spider_up_topic import item_status
status = item_status.Vidoe_Item_Status()
# 定义标签和对应的值的字典
options = {
    "爬取入库": status.is_spider_to_db,
    "下载本地": status.is_download_local,
    "抽帧到wx公众号": status.is_up_4_pic_to_wx,
    "人工质检通过": status.is_human_ok,
    "投稿成功": status.is_tougao_success,
    "错误原因": status.error_reason
}

# 显示selectbox组件
def get_data_from_mongodb_by_page(table_name,page_number, page_size=5):
    # 过滤条件
    selected_values=st.session_state.get('selected_values')
    print(selected_values)


    db = get_db()
    table = db[table_name]
    skip_count = (page_number - 1) * page_size
    # 查询数据并应用分页逻辑
    cursor = table.find({'step':{'$in':selected_values}}).skip(skip_count).limit(page_size)
    page_data=list(cursor)
    print(len(page_data))
    
    return pd.DataFrame(page_data)

# 标记水印位置
from PIL import Image, ImageDraw
def draw_line_on_image(image_path, slider_value):
    response = requests.get(image_path)
    image = Image.open(BytesIO(response.content))
    # image = Image.open(image_path)
    width, height = image.size
    line_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(line_image)
    draw.line([(0, slider_value), (width, slider_value)], fill="red", width=3)
    combined_image = Image.blend(image, line_image, alpha=0.5)
    return combined_image


# 数据列表
def db_tables():
    # 获取数据库中所有表名
    tables=get_db().list_collection_names()
    with st.sidebar:
        selected_table = st.radio(label='选择表', options=tables)
        if selected_table != st.session_state.get('choose_table'):
            st.session_state['choose_table'] = selected_table



# 列表页
def list_part():

    db=get_db()
    choose_table=st.session_state['choose_table']
    total_pages= db[choose_table].count_documents({})//st.session_state['page_size']+1
    # 显示multiselect组件
    selected_labels = st.multiselect("选择标签", list(options.keys()))
    selected_values = [options[label] for label in selected_labels]
    if selected_values!=st.session_state.get('selected_values'):
        st.session_state['selected_values'] = selected_values

    col1,col2=st.columns(2)
    with col1:
        page_number=st.slider('页码', min_value=1, max_value=total_pages, step=1, value=st.session_state.get('page_number') )
    with col2:  
        page_size = st.number_input(label='每页显示数量', min_value=1, step=1, value=st.session_state['page_size'])
        
    
    # 如果页码发生变化，更新数据
    if page_number != st.session_state.get('page_number') or page_size != st.session_state.get('page_size'):
        st.session_state['page_number'] = page_number
        st.session_state['page_size'] = page_size
    
    # 上面的变动引起重新渲染 导致这里发生了不一致
    data_df = get_data_from_mongodb_by_page(choose_table, page_number, page_size)
    if data_df.empty:
        st.error("没有数据")
        return
    if data_df.values!=st.session_state.get('data_df').values:
        st.session_state['data_df'] = data_df


    df_with_selections = data_df.copy()
    try:
        df_with_selections.insert(0, "Select", False)
    except Exception as e:
        pass

    edited_df = st.data_editor(df_with_selections,
                               column_config={"Select": st.column_config.CheckboxColumn(required=True),
                               },
                               num_rows="dynamic",
                               )
    # 选择逻辑
    selected_rows = edited_df[edited_df.Select]
    if selected_rows.values!=st.session_state.get('selected_rows').values:
        st.session_state['selected_rows'] = selected_rows

    # 新增逻辑
    old_last_row = data_df.tail(1)
    new_last_row = edited_df.tail(1)
    if not new_last_row['_id'].equals(old_last_row['_id']):
        key=new_last_row['key'].values[0]
        if not(key):
            return
        item=new_last_row.to_dict('records')[0]
        item['_id']=md5(key)
        del item['Select']
        db[choose_table].update_one({'_id':item['_id']},{'$set':item},upsert=True)
        #   table.update_one({'_id':_id},{'$setOnInsert':item},upsert=True)
        
        
        
        
        
        print("发生了新增",)

        
        
        
def video_length_to_seconds(time_str):
    # 分割分钟和秒钟部分
    minutes, seconds = map(int, time_str.split(':'))
    # 将分钟和秒钟转换为总秒数
    total_seconds = minutes * 60 + seconds
    return total_seconds

def seconds_to_video_length(seconds):
    # 计算分钟和秒钟部分
    minutes = seconds // 60
    seconds_remainder = seconds % 60
    # 格式化为分秒形式字符串
    time_str = '{:02d}:{:02d}'.format(minutes, seconds_remainder)
    return time_str


# 详情页
def detail_part():
    # 针对b站的水印进行标注的详情页   要标注反馈一些信息到monggo
    selected_rows:pd.DataFrame=st.session_state['selected_rows']
    selected_rows_obj=selected_rows.values.tolist()
    filed_name=selected_rows.columns.to_list()
    if len(selected_rows_obj)==0:
        return
    if 'bvid' not in filed_name:
        return
    
    # 获取字段值
    def get_ziduan(ziduan):
        try:
            bvid_indexof=filed_name.index(ziduan)
            bvid=selected_rows_obj[0][bvid_indexof]
            return bvid
        except Exception as e:
            return None
        
    # 最终修改字段显示
    _id=get_ziduan("_id")
    mid=get_ziduan("mid")
    length=get_ziduan("length")
    shuiyin_bili=get_ziduan("shuiyin_bili")
    shijianzhou_delete_length=get_ziduan("shijianzhou_delete_length")

    if shuiyin_bili==None or shijianzhou_delete_length==None:
        shuiyin_bili=0.2
        shijianzhou_delete_length=3

    st.session_state['shijianzhou_delete_length']=shijianzhou_delete_length
    st.session_state['shuiyin_bili']=shuiyin_bili

    shijianzhou_changdu=video_length_to_seconds(length)

# 时间轴标注结果part  有一个old  一个new
    shijianzhou_ele,shijianzhou_res=st.columns(2)
    with shijianzhou_ele:
        new_shijianzhou_delete_length = st.slider("标注时间轴", 0, shijianzhou_changdu,st.session_state['shijianzhou_delete_length'])


    with shijianzhou_res:
        shijianzhou_res_info=seconds_to_video_length(new_shijianzhou_delete_length)
        st.text_input(label="从头删除到",value=shijianzhou_res_info)

    # 用户进行修改后   肯定以用户为准
    if new_shijianzhou_delete_length!=st.session_state.get('shijianzhou_delete_length'):
        st.session_state['new_shijianzhou_delete_length'] = new_shijianzhou_delete_length
        st.success(f"用户侧认为这个结果不对,需要重新修改: {new_shijianzhou_delete_length}")



    #视频显示 
    bvid_indexof=filed_name.index('bvid')
    bvid=selected_rows_obj[0][bvid_indexof]
    videod_url=f'https://player.bilibili.com/player.html?bvid={bvid}'
    iframe_table=f"""<iframe id="my-iframe" src="{videod_url}" width="100%" height="800px" frameborder="0"></iframe>"""
    with st.expander("点击展开/收起原视频"):
        st.markdown(iframe_table, unsafe_allow_html=True)

    # 图片显示
    pic_list=get_ziduan("all_wx_frame_pic_urls")
    if '[' in pic_list and type(pic_list)==str:
        pic_list=eval(pic_list)

    pic=pic_list[0]
    response = requests.get(pic)
    image = Image.open(BytesIO(response.content))
    # image = Image.open(pic)
    width, height = image.size
    shuiyin_info,shuiyin_res=st.columns(2)

    with shuiyin_info:
        new_shuiyin_height = st.slider("标注水印位置", 0.0, float(height), float(height*st.session_state['shuiyin_bili']),step=1.0)
        new_shuiyin_bili=new_shuiyin_height/height
    with shuiyin_res:
        st.text_input(label="当前水印比例",value=new_shuiyin_bili)

    if new_shuiyin_bili!=st.session_state['shuiyin_bili']:
        st.session_state['new_shuiyin_bili']=new_shuiyin_bili
        st.success(f"用户侧认为这个结果不对,需要重新修改: {new_shuiyin_height}")

    if st.button("点击提交确认 水印和长度没问题"):
        # 提交修改
        table=get_db()[st.session_state['choose_table']]
        table.update_one({"_id":_id},{"$set":{
            "step":3,
            "new_shuiyin_bili":new_shuiyin_bili,
            "new_shijianzhou_delete_length":new_shijianzhou_delete_length
            }})
        table.update_many({"mid":mid},{"$set":{"shuiyin_bili":new_shuiyin_bili,"shijianzhou_delete_length":new_shijianzhou_delete_length}})


    with st.expander("点击展开/收起片段的原图",expanded=True):
        combined_image_first = draw_line_on_image(pic, new_shuiyin_height)
        st.image(combined_image_first)
        for pic in pic_list[1:]:
            combined_image_other = draw_line_on_image(pic, new_shuiyin_height)
            st.image(combined_image_other)




def main(*args):
    # 侧边栏
    db_tables()
   
  

    # 主体内容
    list, detail = st.columns(2,gap='small')
    with list:
        list_part()


    with detail:
        detail_part()



    pass


if __name__ == '__main__':
    main()

""""
streamlit run app.py
"""