#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/21 18:11
@Author  : YaoKun
@Usage   : python txt2png2
"""


# 导入需要的包
from PIL import Image, ImageDraw, ImageFont
import string
import os

# 背景尺寸
# 生成一张尺寸为 1350*330 背景色为透明的图片
bg_size = (1350, 330)
# bg = Image.new('RGB', bg_size, color=(0, 62, 140))
bg = Image.new('RGBA', bg_size)

# 字体大小
font_size = 88
# 文字内容
text = '朝阳易捷城市配送有限公司'

# 字体文件路径
font_path = os.path.join('C:/Windows', 'fonts', 'SimHei.ttf')
# 设置字体
font = ImageFont.truetype(font_path, font_size)
# 计算使用该字体占据的空间
# 返回一个 tuple (width, height)
# 分别代表这行字占据的宽和高
text_width = font.getsize(text)
draw = ImageDraw.Draw(bg)

# 计算字体位置
text_coordinate = int((bg_size[0] - text_width[0]) / 2), int((bg_size[1] - text_width[1]) / 2)
# 写字
draw.text(text_coordinate, text, (255, 255, 255), font=font)

# 要保存图片的路径
img_path = os.path.join('D:\\output.png')
# 保存图片
bg.save(img_path)
print('保存成功 at {}'.format(img_path))