import json
import base64
import pychrome
from pychrome.tab import Tab
"""

pip install pychrome -i https://pypi.tuna.tsinghua.edu.cn/simple 

"""
import os
os.environ["DEBUG"] = "True"

def save_screenshot(url, save_path):
    # 创建一个 Chrome 实例
    browser = pychrome.Browser()

    # 新建一个页面
    tab:Tab = browser.new_tab()
    # 启动页面
    tab.start()

    # 打开指定 URL
    tab.Page.navigate(url=url)    # 等待页面加载完成
    tab.wait(5)

    # 获取页面截图
    screenshot = tab.Page.captureScreenshot(format="png")

    # 保存截图到文件
    with open(save_path, "wb") as f:
        f.write(base64.b64decode(screenshot["data"]))

    # 关闭页面
    tab.stop()

    # 关闭 Chrome 实例
    browser.close_tab(tab)

    print("Screenshot saved to", save_path)

if __name__ == '__main__':
    save_screenshot("https://live.douyin.com/255944450985", "screenshot.png")
