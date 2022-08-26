#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2022/2/15 15:25
@Author  : YaoKun
@Usage   : python demo
"""

import os

[d for d in os.listdir('.')]
# print(os.listdir('.'))

# x % 2 == 0  # 取余
# 输出偶数
[x for x in range(1, 11) if x % 2 == 0]

# 筛选出仅偶数的平方
[x * x for x in range(1, 11) if x % 2 == 0]

# 奇数为负
[x if x % 2 == 0 else -x for x in range(1, 11)]

L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [s.lower() for s in L1 if isinstance(s, str)]
# 测试:
print(L2)
if L2 == ['hello', 'world', 'apple']:
    print('测试通过!')
else:
    print('测试失败!')

