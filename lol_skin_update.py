#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : https://www.52pojie.cn/forum.php?mod=viewthread&tid=1580303
@Usage   : python lol_skin_update.py
"""

import requests
from lxml import etree
import os
import time
import zipfile
import shutil  #删除模块
 
#v1.1
 
def download(url, filename):
    start = time.time() #下载开始时间
    try:
        response = requests.get(url, stream=True)  # 来获取服务器的原始套接字响应
        size = 0  # 初始化已下载大小
        chunk_size = 1024  # 每次下载的数据大小
        content_size = int(response.headers['content-length'])  # 下载文件总大小
        if response.status_code == 200:     #判断是否响应成功
            print('Start download,[File size]:{size:.2f} MB'.format(size = content_size / chunk_size /1024))   #开始下载，显示下载文件大小
            with open(filename, 'wb') as f:     #显示进度条
                for data in response.iter_content(chunk_size=chunk_size):   #边下载边存储
                    f.write(data)
                    size += len(data)
                    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
        end = time.time()   #下载结束时间
        print('Download completed!,times: %.2f秒' % (end - start))  #输出下载用时时间
    except:
        print('可能存在网络问题，下载失败，请重试')
        os.system('pause')
        exit()
 
 
def del_dir():     #删除原有文件夹
    path = os.getcwd()
    files = os.listdir(path)
    try:
        for file in files:
            if 'MODSKIN' in file:
                path = path + '\\' + file
                print(path)
                shutil.rmtree(path)
                print('成功删除'+ path)
 
    except:
        print('删除旧文件夹失败或未找到')
 
 
def unzip_file(filename, dir):
    if(zipfile.is_zipfile(filename)):
        fz = zipfile.ZipFile(filename, 'r')     #读取zip文件
        for file in fz.namelist():  #返回压缩包内所有文件名的列表。
            fz.extract(file, dir)    #将zip文档内的指定文件解压到当前目录
        print('解压成功')
    else:
        print('解压失败')
 
 
def start():
    url = 'http://leagueskin.net/p/download-mod-skin-2020-chn'
    try:
        result = requests.get(url).content
    except:
        print('无法连接网络')
        exit()
    soup = etree.HTML(result)
    down_url = soup.xpath('//a[@id="link_download3"]/@href')  # 内容提取
    down_url = down_url[0]
    filename = str(down_url).split('/')
    filename = filename[3]
    dir_name = filename.replace('.zip', '')
    if not os.path.exists(dir_name):
        print("开始处理，请等待")
        del_dir()
        download(down_url, filename)
        dir = os.path.join(os.getcwd(), dir_name)
        unzip_file(filename, dir)
        try:
            print('尝试删除压缩包')
            file_path = os.path.join(os.getcwd(), filename)
            print(file_path)
            os.remove(file_path)
            print('删除成功')
        except:
            print('删除失败')
    else:
        print("没有更新的版本")
    os.system('pause')
 
 
if __name__ == '__main__':
    start()
