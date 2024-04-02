
# # 修正封面
# @retry(max_attempts=5, delay=2)
# def fix_index_img():
#     if not(workder_tab.ele("@@text()=选择封面").click()):
#         raise ValueError("选择封面未找到")
#     time.sleep(2)
    
#     if not(workder_tab.ele("@@text()=上传封面").click() ):
#         raise ValueError("上传封面按钮未找到")
#     time.sleep(2)

#     workder_tab.set.upload_files(index_local_path)
#     workder_tab.ele("@@text()=点击上传 或直接将图片文件拖入此区域").parent().click()
#     time.sleep(2)
#     workder_tab.wait.upload_paths_inputted()
#     ok_ele=workder_tab.ele("@@text()=重新选择").next()

#     if ok_ele.text!="完成":
#         raise ValueError("没有最终非共面判定元素!")

#     return  True

# flag33=fix_index_img()
