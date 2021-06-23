#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/17 11:21
@Author  : YaoKun
@Usage   : python 9x9_2
"""

i = 1
while i < 10:
    j = 1
    while i >= j:
        # print(i, 'x', j, '=', i * j)
        # print(f"{i}x{j}={i * j}")
        print("%sx%s=%-3s" % (i, j, i * j), end='')
        j += 1
    print("")
    i += 1
