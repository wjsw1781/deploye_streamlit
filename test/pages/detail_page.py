
import streamlit as st
from pymongo import MongoClient

def get_mongo_collection():
    client = MongoClient('mongodb://localhost:27017/')  # 连接 MongoDB
    db = client['your_database_name']  # 替换为你的数据库名称
    collection = db['your_collection_name']  # 替换为你的集合名称
    return collection

def get_data_from_mongo():
    collection = get_mongo_collection()
    data = collection.find()  # 获取所有文档数据
    return data

def display_detail_page():
    st.title("Detail Page")
    
    data = get_data_from_mongo()  # 从 MongoDB 获取数据
    
    selected_item = st.selectbox("Select an item", [item["_id"] for item in data])  # 显示下拉框选择项
    
    for item in data:
        if item["_id"] == selected_item:
            st.write(item)  # 显示选定项的详细内容
