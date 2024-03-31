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

import streamlit as st

def display_list_page():
    st.title("List Page")
    
    data = get_data_from_mongo()  # 从 MongoDB 获取数据
    
    for item in data:
        st.write(item)  # 显示每个文档的内容
