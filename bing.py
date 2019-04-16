import time
import threading
import re
import requests


class Request(object):
    # 伪装头部信息
    head = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  '}

    # 得到网页文本信息
    @staticmethod
    def get_text(url):
        try:
            r = requests.get(url, headers=Request.head, timeout=30)
            return r.text
        except Exception as e:
            print(e)

    # 得到图片二进制信息
    @staticmethod
    def get_content(url):
        try:
            r = requests.get(url, headers=Request.head, timeout=30)
            return r.content
        except Exception as e:
            print(e)


# 保存图片为本地文件
def save(text, path, mode="w"):
    with open(path, mode) as f:
        f.write(text)


path0 = "D:\\images\\"  # 文件保存路径
url0 = "https://bing.ioliu.cn/?p="  # bing壁纸链接api

jpgRe = 'url=(.+?)&'  # 筛选图片正则表达式模板
regex = re.compile(jpgRe, re.S)  # 正则表达式


# 得到第pageIndex页图片
def getOnePage(pageIndex):
    pageIndex = str(pageIndex)
    # 打印开始信息
    print("download:", pageIndex)

    # 获得编号为pageIndex的网页
    html_doc = Request.get_text(url0 + pageIndex)
    if html_doc == None:
        # 若失败，打印错误信息
        print("lost:", pageIndex)
        return

    urlList = regex.findall(html_doc)
    # 在当前网页，筛选出全部下一层图片链接，得到一个列表

    for index, value in enumerate(urlList):
        # 对列表遍历，下载所有图片

        # 调用api，下载当前页壁纸
        url = value + "?force=download"

        # 得到url处，壁纸
        text = Request.get_content(url)
        if text == None:
            # 若失败，打印错误信息
            print("lost:", url)
            continue

        # 命名并保存图片
        path = path0 + pageIndex + "_" + str(index) + ".jpg"
        save(text, path, mode="wb")

        # 打印成功提示
        print("get:", url)

    # 打印结束信息
    print("over:", pageIndex)


# 多线程下载bing壁纸
# 并维护线程池

size = 0  # 当前线程池大小
thList = []  # 存储线程

for pageIndex in range(1, 64):
    # 开启下载pageIndex的线程
    th = threading.Thread(target=getOnePage, args=[pageIndex])
    th.start()
    time.sleep(2)

    if size >= 3:
        # 若线程到达4，
        # 清理结束当前线程池
        for th in thList:
            th.join()
        size = 0
    else:
        # 加入线程池
        thList.append(th)
        size += 1