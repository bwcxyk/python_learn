#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/5/31 13:28
@Author  : YaoKun
@Usage   : python main.py
运输许可证ocr
"""

import requests
import base64

url = "https://ocr.cn-north-4.myhuaweicloud.com/v2/0c89b6a390800f392f88c0008eb98455/ocr/transportation-license"
token = "用户获取得到的实际token值"
headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}

imagepath = r'./data/transportation-license-demo.png'
with open(imagepath, "rb") as bin_data:
    image_data = bin_data.read()
image_base64 = base64.b64encode(image_data).decode("utf-8")  # 使用图片的base64编码
payload = {"image": image_base64}  # url与image参数二选一
response = requests.post(url, headers=headers, json=payload)
print(response.text)
