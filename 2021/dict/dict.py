#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/21 15:13
@Author  : YaoKun
@Usage   : python dict
"""

# ⽣生成一个包含100个key的字典，每个value的值不不能一样

info = {

}

for i in range(100):
    info[i] = [i]

for i in info:
    print(i, info[i])

