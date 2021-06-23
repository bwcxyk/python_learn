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

# {'k0': 0, 'k1': 1, 'k2': 2, 'k3': 3, 'k4': 4, 'k5': 5, 'k6': 6, 'k7': 7, 'k8': 8, 'k9': 9} 请把这个dict中key大于5的值value打印出来

# a = {'k0': 0, 'k1': 1, 'k2': 2, 'k3': 3, 'k4': 4, 'k5': 5, 'k6': 6, 'k7': 7, 'k8': 8, 'k9': 9}
# for i in a:
#     # print(i, a[i])
#     print(a[i])

