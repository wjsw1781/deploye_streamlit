pyhton3.8


python -m venv myenv

C:\projects\py_win\myenv\Scripts\activate.bat

python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple  


git checkout --orphan  fix 
git add -A 
git commit -am "fix ok" 
git branch -D main
git branch -m main
git remote add gitee https://gitee.com/wang_zhi_quan/deploy_streamlit.git
git remote add github https://github.com/wjsw1781/deploye_streamlit.git

git push -f -u gitee "main"
git push -f -u github "main"

<!-- 直接删除远程仓库和本地的联系 -->
git remote remove gitee
git remote remove github
<!-- 删除远程origin仓库的main分支 -->
git push origin --delete main


pip install loguru requests  httpx moviepy==1.0.3 numpy==1.21.5 opencv_python==4.5.5.62   pandas -i https://pypi.tuna.tsinghua.edu.cn/simple  

pip install loguru  numpy==1.21.5    pandas -i https://pypi.tuna.tsinghua.edu.cn/simple  
pip install bilibili-api-python  moviepy  pandas -i https://pypi.tuna.tsinghua.edu.cn/simple  
pip install redis -i https://pypi.tuna.tsinghua.edu.cn/simple  

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple  

pip install bilibili-api-python

使用一个工具似乎更容易控制浏览器  当然js的能力也要建设起来!!!!
但是它太好用了 cdp似乎做的事情更牛逼 更确定!!!



爬取
筛选
人工标记审核平台
剪辑
上传


<!-- 关于可视化审核平台的初步设想 -->
未来肯定会有很多表作为业务线出现 本质上都是对状态的查看  以及修改 
但是不同的表需要的查看和修改逻辑并不一样  但本质上都是以字段为单位进行修改
所以可以抽离出三个实体

原始表格以及字段内容
展示表格和字段的组件
最终detail页结果

数据+组件=detail页

未来只是新增组件和数据源   即可

比如业务
        显示s3上的图片并进行逐个审核
        显示资产详情
        标注视频尺寸 水印
本质上都是对状态的查看  以及修改


b站爬取的任何主题的视频都要增加两个字段一个水印信息 一个时间轴移除信息
shuiyin_bili
shijianzhou_delete_length

人工质检可能会新增额外的两个
new_shuiyin_bili
new_shijianzhou_delete_length

初步确认 二次确认

最后一个就是阿里云要部署streamlit进行查看  还要对每个视频存储4张截图(可以存放到微信公众号 但是感觉不稳定有变数)





