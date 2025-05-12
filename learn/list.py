#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author : yaokun
@Time : 2020/9x9/4 15:33
"""

import sys

list = [1, 2, 3, 4]
it = iter(list)  # 创建迭代器对象
while True:
    try:
        print(next(it))
    except StopIteration:
        sys.exit()