#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2021/03/28 11:08
@Author  : YaoKun
@Usage   : python main.py file.xlsx
"""

from multiprocessing.pool import ThreadPool
from queue import Queue

import openpyxl
import requests
import sys


def download(file_name, url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like" \
                 " Gecko) Chrome/87.0.4280.67 Safari/537.36"
    headers = {'User-Agent': user_agent}
    resp = requests.get(url.strip(), headers=headers, stream=True)
    with open(f'./{file_name}.pdf', 'wb') as w:
        w.write(resp.content)
    print(f'{file_name} 下载完成')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        q = Queue()
        pool = ThreadPool(10)
        filename = sys.argv[1]
        sheet = openpyxl.open(filename).get_sheet_by_name('Sheet1')
        for item in sheet.rows:
            q.put([item[0].value, item[1].value])
        q.get()
        while not q.empty():
            pool.apply_async(download, args=q.get())
        pool.close()
        pool.join()
    else:
        print('Usage: python %s file.xlsx' % sys.argv[0])
