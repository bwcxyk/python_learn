#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/9/13 9:30
@Author  : YaoKun
@Usage   : python config
"""

import yaml
import os


def get_yaml_data(yaml_file):
    # 打开yaml文件
    # print("***获取yaml文件数据***")
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    # print(file_data)
    # print("类型：", type(file_data))

    # 将字符串转化为字典或列表
    # print("***转化yaml数据为字典或列表***")
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    # print(data)
    # print("类型：", type(data))
    return data

# if __name__ == '__main__':
#     current_path = os.path.abspath("..")
#     yaml_path = os.path.join(current_path, "config.yaml")
#     get_yaml_data(yaml_path)
