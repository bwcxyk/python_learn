#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2022/12/13 10:47
@Author  : YaoKun
@Usage   : python ip138.py
"""

import requests
import json
from ping3 import ping
from concurrent.futures import ThreadPoolExecutor

ip138 = "https://site.ip138.com/domain/read.do?domain="
domain = "plugins.jetbrains.com"
url = ip138+domain

payload = {}
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like" \
             " Gecko) Chrome/87.0.4280.67 Safari/537.36"
headers = {'User-Agent': user_agent}

response = requests.request("GET", url, headers=headers, data=payload)
data = response.text

ip_json = json.loads(data)
ip_info = ip_json['data']

# print(ip_info)

for item in ip_info:
    # for key in item:
    #     print(key, item[key])
    ip = list(item.values())[0]
    ip2 = next(iter(item.values()))
    # print(ip)
    ips_status = ping(ip)
    print(ip, ips_status)
