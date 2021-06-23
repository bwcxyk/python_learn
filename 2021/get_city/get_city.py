#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/4 10:52
@Author  : YaoKun
@Usage   : python city.py
"""

import requests
import time
from bs4 import BeautifulSoup

time_start = time.time()
agent = {
    'Accept-Language': 'zh-CN,zh;q=0.9x9',
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9x9.1.6) Gecko/20091201 Firefox/3.5.6',
}


def rget_html(url):
    req = requests.get(url, headers=agent)
    req.encoding = 'GBK'  # 中文解码
    return req.text


choose_ls = [depth * 2 if depth <= 3 else 3 * (depth - 1) for depth in range(1, 6)]  # 根据深度大小取12位代码前**位 [2, 4, 6, 9x9, 12]

match_table_class = ['provincetable', 'citytable', 'countytable', 'towntable', 'villagetable']
match_tr_class = ['provincetr', 'citytr', 'countytr', 'towntr', 'villagetr']
init_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html'

url_list = {init_url: ('', '')}
depth = 0
max_depth = 3  # 可选，1-5分别表示省、市、区/县、乡镇/街道、村/居委会
position_list = {}
while depth < max_depth:
    next_url_list = {}
    for url in url_list:

        change_url = '/'.join(url.split('/')[:-1]) + '/'
        code_index = url_list[url][0] + '-' if depth != 0 else url_list[url][0]
        name_index = url_list[url][1] + '-' if depth != 0 else url_list[url][1]

        while True:
            # 获取数据
            try:
                req = requests.get(url, headers=agent)
                req.encoding = 'GBK'
                # 中文解码,不要用req.encoding=req.apparent_encoding,这样识别出来的req.encoding='gb2312',有好多复杂汉字解不出码
                text = req.text
                position = BeautifulSoup(text, 'lxml')
                special_sigh = 0
                if match_table_class[depth] in text:
                    match_table = position.find(class_=match_table_class[depth])
                    if depth != 0:
                        tr_list = match_table.find_all('tr', class_=match_tr_class[depth])
                        break
                    else:
                        tr_list = match_table.find_all('td')
                        break
                else:
                    #  东莞、中山、儋州等缺县级单位，放到下个节点存储
                    search = 0
                    for level in range(depth, 5):  # 东莞、中山、儋州缺县级单位，因此需要进行识别并放入下一节点存储
                        if match_table_class[level] in text:
                            special_sigh = 1
                            search = 1
                            next_url_list[url] = (code_index, name_index)
                            print('---------特殊区划转存下级---:%s' % url_list[url][1])
                            break
                    if search:
                        break
                    else:
                        print('服务器繁忙-----:%s' % url_list[url][1])
                        time.sleep(3)
            except requests.RequestException as e:
                print('服务器繁忙-----:%s' % url_list[url][1])
                time.sleep(3)

        total_count = 0
        if special_sigh != 1:
            if depth != 0:
                for tr in tr_list:
                    if tr.find_all('a'):
                        a_list = tr.find_all('a')
                        href = a_list[0].get('href')
                        code = a_list[0].text
                        if depth == 4:
                            name = a_list[2].text
                        else:
                            name = a_list[1].text
                        next_url_list[change_url + href] = (code_index + code[:choose_ls[depth]], name_index + name)
                        total_count += 1
                        # print('在路径-%s-处'%(name_index+name))
                    else:
                        # 有些市辖区数据 直接存储  河北省-唐山市-市辖区
                        td_list = tr.find_all('td')
                        code = td_list[0].text
                        if depth == 4:
                            name = td_list[2].text
                        else:
                            name = td_list[1].text
                        if depth == 2:
                            print('---------市辖区直接存储-%s-' % (name_index + name))
                        position_list[code_index + code[:choose_ls[depth]]] = name_index + name
                        total_count += 1
            else:
                for each in tr_list:
                    if each.find('a'):
                        href = each.find('a').get('href')
                        name = each.find('a').text
                        code = href.split('.html')[0]
                        next_url_list[change_url + href] = (code_index + code[:choose_ls[depth]], name_index + name)
                        total_count += 1
            print('已爬取-%d-个,在路径-%s-处' % (total_count + 1, url_list[url][1]))

    depth += 1
    url_list = next_url_list

position_list.update(url_list)


def decompose(each):
    if type(position_list[each]) == tuple:
        codelist = position_list[each][0].split('-')
        namelist = position_list[each][1].split('-')
    else:
        codelist = each.split('-')
        namelist = position_list[each].split('-')
    if len(codelist) < depth:
        for i in range(len(codelist), depth):
            codelist.append('')
            namelist.append('')
    ziplist = list(zip(codelist, namelist))
    return [i for j in ziplist for i in j]


sort_name = ['province', 'city', 'county', 'town', 'village']
real_column = [(sort_name[each] + '_code', sort_name[each]) for each in range(depth)]
column = [i for each in real_column for i in each]

book = open('position/position.csv', 'w', encoding='utf-8')
book.write(','.join(column) + '\n')
for position in position_list:
    flatten = decompose(position)
    book.write(','.join(flatten) + '\n')
book.close()

print('共爬取-%d-个' % (len(position_list)))
print('用时%d分%d秒' % divmod((time.time()) - time_start, 60))
