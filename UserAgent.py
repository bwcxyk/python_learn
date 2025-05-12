#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@Time    : 2020/12/8 11:43
@Author  : YaoKun
"""
import fake_useragent

location = 'E:/fake_useragent%s.json' % fake_useragent.VERSION
ua = fake_useragent.UserAgent(path=location)

print(ua.ie)   # 随机打印ie浏览器任意版本
print(ua.firefox)   # 随机打印firefox浏览器任意版本
print(ua.chrome)  # 随机打印chrome浏览器任意版本
print(ua.safari)
print(ua.opera)
print(ua.random)  # 随机打印任意厂家的浏览器
