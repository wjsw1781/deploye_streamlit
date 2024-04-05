import os
from PIL import Image, ImageDraw, ImageFont




when_import_the_module_the_path=os.path.dirname(__file__)
font_path=f'{when_import_the_module_the_path}/瘦金体.ttf'
font_size=20
font = ImageFont.truetype(font_path, font_size)

from PIL import Image, ImageDraw, ImageFont

# 文字转图片
def generate_transparent_image(text,output_image_path):
                               

    text_color=(255, 255, 255)
    background_color=(255, 255, 255, 0)
    image_width=len(text)*font_size+10

    img = Image.new("RGBA", (image_width, font_size + 10), background_color)
    draw = ImageDraw.Draw(img)

    draw.text((0,0), text,fill=text_color, font=font)
    img.save(output_image_path)

    return img

# 图片加文字
def image_add_text(img_path, text,  savePath,):
    '''
    :param img_path: 图片路径
    :param text: 需要添加的文字
    :param savePath: 图片保存路径
    :return: 
    '''
    if '\n' not in text:
        raise "文本中必须包含\n"
    max_width=len(text.split('\n')[0])


    im = Image.open(img_path).convert("RGBA")
    txt_img = Image.new('RGBA', im.size, (0, 0, 0, 0))
    font_size = (txt_img.size[0] // max_width)
    font_height=text.count('\n')*font_size+font_size
    font_path = r'C:\Windows\Fonts\simsun.ttc'
    tfont = ImageFont.truetype(font_path, size=font_size)
    draw = ImageDraw.Draw(txt_img)
    xz, yz = 20, txt_img.size[1]//2 

    shape=[0, yz, txt_img.size[0], yz+font_height]
    rect_color = (22, 255, 130, 360)  # 矩形颜色和透明度
    draw.rectangle(shape, fill =rect_color,) 


    # (0, 0, 0, 180):前三个数代表RGB（范围0-255），最后一个数代表透明度
    draw.text((xz, yz), text=text, fill=(255, 0, 0, 360), font=tfont)

    out = Image.alpha_composite(im, txt_img)
    out = out.convert('RGB')
    out.save(savePath)


# 文字转 横向流程图 
def generate_horizontal_process_flow(steps):
    # 定义方块的尺寸和间距
    block_width = 200
    block_height = 100
    block_padding = 20
    font_size = 14
    
    # 计算画布尺寸
    num_steps = len(steps)
    canvas_width = (block_width + block_padding) * num_steps + block_padding
    canvas_height = block_height + block_padding * 2
    
    # 创建白色背景图像  操作draw对象
    img = Image.new('RGB', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(img)
    
    # 定义颜色映射
    color_map = {
        'ok': 'green',
        'running': 'yellow',
        'error': 'red'
    }
    
    # 绘制每个步骤
    for i, step in enumerate(steps):
        x = i * (block_width + block_padding) + block_padding
        # 确定背景颜色
        status = step['step']
        if status in color_map:
            color = color_map[status]
        else:
            color = 'gray' # 默认为灰色
        
        # 绘制方块
        draw.rectangle([x, block_padding, x + block_width, block_padding + block_height], fill=color, outline='black')
        
        # 绘制文字
        name = step['name']
        if step['error']:
            name += ' (' + step['error'] + ')'
        draw.text((x + 10, block_padding + 10), name, font=font, fill='black')
    
    return img




if __name__ == '__main__':
    # 示例用法
    generated_image_path = image_add_text(f"{when_import_the_module_the_path}/龙珠封面.png","龙珠Z_人造人篇_该死的沙鲁\n龙珠Z_人造人篇_该死的沙鲁", "img_add_text.png")

    
    # 生成图片
    image = generate_transparent_image("永远热爱",  "text_2_img.png")

    # 生成流程图
    # 测试生成流程图
    steps = [
        {'name': '下载本地', 'step': 'ok', 'error': False},
        {'name': '制作封面', 'step': 'ok', 'error': False},
        {'name': '投稿', 'step': 'running', 'error': False}
    ]

    process_flow_img = generate_horizontal_process_flow(steps)
    process_flow_img.save('text_2_flow.png')