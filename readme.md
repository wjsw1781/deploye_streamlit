pyhton3.8


python -m venv myenv

C:\projects\py_win\myenv\Scripts\activate.bat

python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple  

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple  

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

pip install streamlit -i https://pypi.tuna.tsinghua.edu.cn/simple  

pip install loguru  numpy==1.21.5    pandas -i https://pypi.tuna.tsinghua.edu.cn/simple  
pip install bilibili-api-python  moviepy  pandas -i https://pypi.tuna.tsinghua.edu.cn/simple  
pip install redis -i https://pypi.tuna.tsinghua.edu.cn/simple  


pip install bilibili-api-python

pip freeze > C:\projects\py_win\requirements.txt

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



浏览器回填路径上传也有字符问题 统一修改成window可识别的路径  后面又确认了下 是本地文件不存在导致的




2024年4月4日  重新设计了下架构  就是环节是环节 状态是状态   

初始化  爬取  抽帧    审核   上传   评论  引流  api上屏app分享    

每一个环节都有三个状态 进行中  失败  成功   成功才会进入下一个状态

最终使用gradio还是streamlit 我到现在还没想通透  似乎峰回路转了
暂定gradio 因为streamlit移动端无法布局和移动点击拖拽! 太尴尬了!  gradio页不能进行这个操作  手机端死活加载不出来 哎



新的流程定了
ui加载bilibili的搜索页面  这样就能控制话题了 两个iframe显示列表和detail  然后直接一个df进行操控 完美  直接解决了审核流程,开始就是审核  好的内容驱动开始   这里就可以判定水印位置了


然后是下载


然后是剪辑


然后是上传

话题是话题 热点是热点  我这里还要抽象

大型记录篇是一个话题 ---------------->技师足浴按摩是热点  操作的是一个表:大型记录片

后面就是发现好的视频抽象成一个大的话题 建立一个表 前端人工搜索 后端主动通过up主爬取 两个方向入库 ! 下载!  人工确认!  剪辑! 投稿!


大型纪录片 --> 很多up主
治愈      --> 固定几个up主
预告片    --> 固定几个up主
美丽风景  --> 固定几个up主




环节状态设置 我又加强了 由于一些调试和业务改动 导致新增状态或者环节 总是会导致一些重要状态被重置 此时难以维护和同步  就算写道mogno数据库  又会引发严重对mongo的修改
所以每个环节中都会进行文件系统的打标签 甚至是二次确认标签  保证不会受到那个抽象环节的状态的频繁修改所带来的影响


环节状态更像是给用户查看的  对查看的!!!!!   所有业务没有必要参考这个  只要参考本身的文件系统标签就行了

































