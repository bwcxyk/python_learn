#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@Time    : 2020/10/19 14:13
@Author  : YaoKun
@Usage   : python down.py
"""

# -*- coding: utf-8 -*-
#  根据文件链接列表获取文件保存到本地

from urllib.request import urlretrieve
import os
# 解决
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

'''
通过txt网址文件，下载文件到本地
'''
def download():
    categories = ['file']
    for category in categories:
        # 新建存储file文件夹存储文件
        os.makedirs('data/%s' % category, exist_ok=True)
        # 读取txt文件
        with open('%s.txt' % category, 'r') as file:
            urls = file.readlines()
            # 计算链接地址条数
            n_urls = len(urls)
            # 遍历链接地址下载文件
            for i, url in enumerate(urls):
                try:
                     # 请求下载文件，并截取最后链接第一最后一节字段命名文件
                     urlretrieve(url.strip(), 'data/%s/%s' % (category, url.strip().split('/')[-1]))
                     print('%s %i/%i' % (category, i, n_urls))
                except:
                     print('%s %i/%i' % (category, i, n_urls), 'no image')

if __name__ == '__main__':
    download();