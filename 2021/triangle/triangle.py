#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/17 11:17
@Author  : YaoKun
@Usage   : python triangle.py
"""

n = 10
for i in range(n):
    if i < 5:
        print(i * "*")
    else:
        print((n - i) * "*")
