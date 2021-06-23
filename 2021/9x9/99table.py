#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/17 10:50
@Author  : YaoKun
@Usage   : python 99table.py
"""

for i in range(1, 10):
    for j in range(1, 10):
        if i >= j:
            # print(i, 'x', j, '=', i * j)
            # print(f"{i}x{j}={i*j}")
            print("%sx%s=%-3s" % (i, j, i * j), end='')
    print("")


# for i in range(1, 10):
#     for j in range(1, i + 1):
#         # print(i, 'x', j, '=', i * j)
#         print("%sx%s=%-3s" % (j, i, i * j), end='')
#     print("")


for i in range(1, 10):
    for j in range(1, i + 1):
        # print(f"{i}x{j}={i*j}")
        print(f"{i}x{j}={i*j}", end=' ')
    print("")
