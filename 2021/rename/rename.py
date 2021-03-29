#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2021/3/26 17:55
@Author  : YaoKun
@Usage   : python rename.py file.xlsx
"""

import os
import sys
import pandas as pd

# os.chdir(r'C:\Users\Administrator\Desktop\2021-3-26')

cwd = os.getcwd()
items = os.listdir(cwd)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        wb = pd.read_excel(filename)
        print("重命名开始")
        print("-------------------")
        for i in items:
            if i in wb['原名'].values:
                idx = wb[(wb['原名'] == i)].index.tolist()
                os.rename(i, wb['新名'][idx[0]])
                # print("文件", i, "已重命名为", wb['新名'][idx[0]])  # 写法不规范
                print("文件", wb['原名'][idx[0]], "已重命名为", wb['新名'][idx[0]])
                print("-------------------")
                print("重命名结束")
    else:
        print('Usage: python %s file.xlsx' % sys.argv[0])