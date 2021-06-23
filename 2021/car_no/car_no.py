#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/17 17:33
@Author  : YaoKun
@Usage   : python car_no.py
"""

import random
import string

# o = "AJKFD98643"
# i = random.sample(o, 2)
# j = "".join(i)
# print(j)


# one = random.sample(string.ascii_uppercase, 1)
# two = random.sample(string.digits + string.ascii_uppercase, 5)
# one_str = "".join(one)
# two_str = "".join(two)
# print(f"沪{one_str}-{two_str}")


car_num_sample = string.digits + string.ascii_uppercase  # 数字和大写字母组合
# print(random.sample(car_num_sample, 5))

count = 3
while count > 0:
    count -= 1
    car_num_list = []
    for i in range(20):
        one_letter = random.choice(string.ascii_uppercase)  # 返回大写字母
        two_letter = "".join(random.sample(car_num_sample, 5))  # 随机返回数字大写字母并转换为字符串
        car_num = f"沪{one_letter}-{two_letter}"  # 返回车牌号组合
        car_num_list.append(car_num)  # 将车牌号加入列表
        print(i+1, car_num)
    choice = input("输入你的选择:").strip()
    if choice in car_num_list:
        exit(f"恭喜你,车牌是{choice}")
    else:
        print(f"未选中，还有{count}次机会")
