#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author : yaokun
@Time : 2020/7/29 14:33
"""


try:
    a = int(input("输入被除数："))
    b = int(input("输入除数："))
    c = a / b
    print("您输入的两个数相除的结果是：", c)
except ArithmeticError:
    print("程序发生了数字格式异常、算术异常之一")
except ValueError:
    print("未知异常")
print("程序继续运行")
