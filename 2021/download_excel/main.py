#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2021/03/28 11:08
@Author  : YaoKun
@Usage   : python main.py file.xlsx
"""

import openpyxl
import requests
import sys
import os
from multiprocessing.pool import ThreadPool
from queue import Queue


def download(file_name, url):
    # 定义用于 HTTP 请求头的用户代理
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
    headers = {'User-Agent': user_agent}
    
    try:
        # 发送带有头信息的 GET 请求到指定的 URL，并以流的形式获取内容
        resp = requests.get(url.strip(), headers=headers, stream=True)
        resp.raise_for_status()  # 检查请求是否成功

        # 从 URL 中获取文件名，保留原有的扩展名
        _, file_extension = os.path.splitext(url)
        file_name_with_extension = f'./{file_name}{file_extension}'
        
        # 将获取的内容写入本地文件
        with open(file_name_with_extension, 'wb') as w:
            w.write(resp.content)
        
        # 打印下载完成的消息
        print(f'{file_name_with_extension} 下载完成')
    except requests.RequestException as e:
        print(f'下载失败: {e}')

def process_excel_file(filename):
    # 打开 Excel 文件并获取名为 'Sheet1' 的工作表
    workbook = openpyxl.open(filename)
    sheet = workbook[workbook.sheetnames[0]]

    q = Queue()  # 初始化用于保存下载任务的队列
    pool = ThreadPool(10)  # 创建一个包含 10 个线程的线程池
    
    try:
        # 为表中的每一行（除了第一行）添加下载任务到队列中
        for item in sheet.iter_rows(min_row=2, values_only=True):
            file_name_base = item[0]  # 假设 item[0] 是表示文件名的字符串
            for index, column_value in enumerate(item[1:], start=1):
                q.put([f'{file_name_base}_{index}', column_value])

        # 获取队列中的任务数量
        num_tasks = q.qsize()

        # 使用线程池并行处理下载任务
        for _ in range(num_tasks):
            pool.apply_async(download, args=q.get())

        pool.close()  # 表示不会再往线程池中添加任务
        pool.join()   # 等待所有线程完成
    finally:
        workbook.close()  # 确保文件被关闭

if __name__ == '__main__':
    # 检查脚本是否以正确数量的命令行参数执行
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        process_excel_file(filename)
    else:
        # 如果未提供正确数量的参数，则打印使用说明
        print('Usage: python %s file.xlsx' % sys.argv[0])
