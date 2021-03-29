#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@Time    : 2020/9/17 14:59
@Author  : YaoKun
"""

f = open("C:/Users/Administrator/Desktop/test.txt", "w")
for n in (x * x for x in range(100)):
    # print(n)
    # print(type(n))
    f.write("{}\n".format(n))
f.close()

fo = open("C:/Users/Administrator/Desktop/test.txt", "r")
re = fo.read()
print("读取的内容是" "\n" + re)
fo.close()