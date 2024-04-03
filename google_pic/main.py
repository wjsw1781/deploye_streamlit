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




from utils.utils import *

chrome=get_one_window_with_out_proxy('google_pic')

key_info=['infographic Great Wall of China']


for ii in key_info :
    url=f"https://www.google.com.hk/search?newwindow=1&sca_esv=1c9bdfbc92b64cc5&sca_upv=1&q={ii}&udm=2&source=univ&fir=whNM5o8IyenJFM%252CbA1yJLtsbFDIFM%252C_%253BH3p-YzPJYeUyNM%252C_UWCAyeN2ZiAUM%252C_%253BP3Egf_gsd_OR0M%252CdLokWWU67rraYM%252C_%253B76BjyLiknvmrNM%252C7zWvOrKaH_bsYM%252C_%253B9MiMlWNo2w3BOM%252C6u914CzNHzat9M%252C_%253BJpRfW8Xy0K9tkM%252C-0UzFLhDg3jyaM%252C_%253BvqUSGnuRX2mJRM%252CtUO5wLaIhpA9mM%252C_%253B96AICnZ-ISqp_M%252CJ3ZquzKZyHe2IM%252C_%253BsJgogEBdJxP-VM%252C-0UzFLhDg3jyaM%252C_%253Bji7ptuTRCwGJSM%252C9h0BYdwsviWUdM%252C_%253BcDyl4TYF4xkBwM%252CDzde7KodS6WxYM%252C_%253BDBseJCIMXMVt9M%252Cbzc6_xQxu_P7CM%252C_&usg=AI4_-kRA8vgA2E8vMWvVFhevvbmwXV5RKA&sa=X&ved=2ahUKEwjGh8_SzKWFAxWXgK8BHSy2C14Q7Al6BAgPEDM&biw=1920&bih=953"
    chrome.get(url)
    for ii in range(3):
        chrome.scroll.to_bottom()
        time.sleep(1)
    #所有小图片
    all_small_pic=chrome.eles('xpath://div[@id="search"]//img')
    guolv_img=[]
    for ii in all_small_pic:
        width=int(ii.width)
        if width>100:
            guolv_img.append(ii)
    for img in guolv_img:
        img.click()
        input()
    input()



