#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2020/10/19 15:08
@Author  : YaoKun
@Usage   : python downfile.py file.txt
"""

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import requests
import sys
# import os


def download(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like" \
                 " Gecko) Chrome/87.0.4280.67 Safari/537.36"
    headers = {'User-Agent': user_agent}
    # filename = url.split('/')[-1].strip()
    # filename = "respose.log"
    r = requests.get(url.strip(), headers=headers, stream=True)
    with open(filename, 'ab+') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        f.flush()
        print(filename, "is ok")


# def removeline(key, filename):
#     os.system('sed -i /%s/d %s' % (key, filename))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        f = open(filename, "r")
        p = Pool(4)
        for line in f.readlines():
            if line:
                p.spawn(download, line.strip())
                # key = line.split('/')[-1].strip()
                # removeline(key, filename)
                f.close()
                p.join()
    else:
        print('Usage: python %s file.txt' % sys.argv[0])
