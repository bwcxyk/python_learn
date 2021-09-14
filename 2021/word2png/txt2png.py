#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/21 17:53
@Author  : YaoKun
@Usage   : python word2png
"""


# 先导入所需的包
import pygame
import os
import pandas as pd

pygame.init()  # 初始化

B = '火蓝科技'  # 变量B需要转图片的文字
text = u"{0}".format(B)  # 引号内引用变量使用字符串格式化
# text=str(pd.read_csv(r'D:\output.csv',encoding='gbk'))
print(text)
# 设置字体大小及路径
font = pygame.font.Font(os.path.join("C:/Windows/Fonts", "SimHei.ttf"), 70)
# font = pygame.font.Font(os.path.join("/Users/akun/Library/Fonts", "msyh.ttf"), 26)
# 设置位置及颜色
rtext = font.render(text, True, (255, 255, 255), (0, 62, 140))

# 保存图片及路径
pygame.image.save(rtext, "D:\output.png")
