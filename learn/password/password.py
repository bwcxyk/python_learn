#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/6/9 14:54
@Author  : YaoKun
@Usage   : python security_group.py
"""


import random
import string


def generate_password(length):
    # 定义包含所有可用字符的字符串
    characters = string.ascii_letters + string.digits + "!@#$%^*()_-+={[}]|\\:\<>,.?/"
    
    # 使用random模块生成随机密码
    password_new = ''.join(random.choice(characters) for _ in range(length))
    
    return password_new


# 设置所需密码的长度
password_length = 12

# 生成密码
password = generate_password(password_length)

# 打印密码
print("生成的密码为:", password)
