
# -*- coding: utf-8 -*-
import sys,os
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

from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage._pages.chromium_tab import ChromiumTab
# -i https://pypi.tuna.tsinghua.edu.cn/simple 



item_name="dy_up"

# 上传抖音
def up_to_dy():
    from_step=video_item.is_human_ok
    end_step=video_item.is_tougao_success
    error_step=video_item.is_tougao_success+video_item.error_reason
    for ii in table_two.find({'step':from_step}):
        try:
            _id=ii['_id']
            safe_title=ii['safe_title']
            local_name = os.path.abspath(f'./assert/{kind}/{safe_title}')
            pic_index = f"{local_name}/index.jpg"
            video_mp4_name = f"{local_name}/video.mp4"
            video_mp4_namegood = video_mp4_name + "good.mp4"

            table_two.update_one({'_id':_id},{'$set':{"step":end_step},})

            logger.success(f"{curent_time}  {safe_title}  投稿过程  __-----__  完成")
        except Exception as e:
            table_two.update_one({'_id':_id},{'$set':{"step":error_step,'error_reason':"裁剪 投稿过程中出错"+str(e)}})



    pass


from utils.utils import *


def main_up_fun():

    pass


chrome:ChromiumPage=get_one_window_with_out_proxy(item_name=item_name)


url='https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page'

merge_to_mp4_file=r"D:\projects\deploy_streamlit\spider_up_topic\assert\大型纪录片\大型纪录片_普通人的一生2_\video.mp4good.mp4"
merge_to_mp4_file=r"C:\projects\py_win\assert\龙珠\0a77385138e1a816bcdd246a6dee88c5\ok.mp4"
title="龙珠z_re"
description="龙珠z_re_永远热爱"


workder_tab=chrome.new_tab(url)

for i in range(10):
    # 证明react成功加载
    root=workder_tab.ele('xpath://div[@id="root"]')
    if root:
        break

# 设置要上传的文件
for i in range(10):
    #证明可以被点击触发视频上传框 
    up_input=workder_tab.ele('xpath://input[@accept="video/mp4,video/x-m4v,video/*"]')

    up_buton=up_input.parent()
    if up_buton:
        break
workder_tab.set.upload_files(merge_to_mp4_file)
up_buton.click() 
workder_tab.wait.upload_paths_inputted()



# 标题
title_input=workder_tab.ele('xpath://input[@placeholder="好的作品标题可获得更多浏览"]')
title_input.input(title)
# 描述
description_input=workder_tab.ele('xpath://*[@data-placeholder="添加作品简介"]')
description_input.input(description)

# 发布按钮
while 1:
    publish_buton=workder_tab.ele('xpath://button[text()="发布"]')
    time.sleep(10)
    if 'manage' in workder_tab.url:
        logger.success(workder_tab.url)
        break
    try:
        publish_buton.click()
    except Exception:
        pass


# if __name__ == '__main__':
#     try:
#         main_up_fun()

#     except Exception as e:
#         tell_to_wx("上传抖音失败  "+str(e))
    


    