#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/18 14:24
@Author  : YaoKun
@Usage   : python lucky_draw.py
"""

import random

employees = []
for i in range(1, 301):
    employees.append(f"员工{i}")
lucky_num = [30, 6, 3]
for i in range(3):
    lucky_man = random.sample(employees, lucky_num[i])
    for s in lucky_man:
        employees.remove(s)
    print(f"抽中{3-i}等奖")
    print(lucky_man)
