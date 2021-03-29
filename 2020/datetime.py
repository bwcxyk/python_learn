#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'YaoKun'
__time__ = '2020/6/8 13:35'

from datetime import datetime
def set_flow():
    base_code = datetime.now().strftime('%Y%m%d%H%M%S')
    oreder_list = []
    count = 1
    while True:
        if count > 50:
            break
        count_str = str(count).zfill(5)
        oreder_list.append(base_code + count_str)
        count += 1
    return oreder_list
a=set_flow()
print(a)