#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/24 17:03
@Author  : YaoKun
@Usage   : python thread
"""

import threading
import time


def read():
    for x in range(5):
        print('在%s,正在听音乐' % time.ctime())
        # time.sleep(1.5)


def main():
    music_threads = []  # 用来存放执行read函数线程的列表

    for i in range(0, 1):  # 创建1个线程用于read()，并添加到read_threads列表
        t = threading.Thread(target=read)  # 执行的函数如果需要传递参数，threading.Thread(target=函数名,args=(参数，逗号隔开))
        music_threads.append(t)
        music_threads[i].start()
        time.sleep(1)

    # for i in range(0, 1):  # 启动存放在read_threads列表中的线程
    #     music_threads[i].start()
    #     time.sleep(1)


if __name__ == '__main__':
    main()
