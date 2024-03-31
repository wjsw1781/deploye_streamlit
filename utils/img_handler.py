from PIL import Image, ImageDraw, ImageFont
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



if __name__ == '__main__':
    # 示例用法
    text = "龙珠Z_人造人篇_该死的沙鲁\n龙珠Z_人造人篇_该死的沙鲁"
    image_path = r"C:\projects\py_win\assert\龙珠\封面\33.png"
    output_path = "output_image.jpg"
    generated_image_path = image_add_text(image_path,text, output_path)

    
    print("生成的图片路径:", generated_image_path)
