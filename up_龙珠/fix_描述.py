

from opencc import OpenCC

from config import table

converter = OpenCC('t2s')  # 't2s'表示繁体转简体


for  i in table.find({}):
    print(i['desc'],i['title'])
    new_desc=i['desc'].replace('快手','抖音')
    new_title=i['title'].replace('快手','抖音').replace('阿b不给力,导致下架!非常可惜,希望抖音能够坚挺!最后,如果喜欢请给原作者_二重转生的欣酱_支持','')

    simplified_chinese_text = converter.convert(new_title)

    table.update_one({"_id":i['_id']},{"$set":{"desc":new_desc,"title":simplified_chinese_text}})