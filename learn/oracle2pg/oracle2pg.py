#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/8 13:52
@Author  : YaoKun
@Usage   : python oracle2pg
"""

import cx_Oracle
import psycopg2
import os
import time
from io import StringIO
import pandas as pd

# 说明：本脚本用于将Oracle数据迁移到PG
# 注意：源表与目标表字段数量必须一致

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 设置字符集为UTF8，防止中文乱码
source_db = cx_Oracle.connect('scott/tiger@192.168.3.10/orcl')  # 源库
target_db = psycopg2.connect(database="orcl", user="scott", password="tiger", host="192.168.56.10", port="5432")  # 目标库
cur_select = source_db.cursor()  # 源库查询对象，打开游标
cur_insert = target_db.cursor()  # 目标库插入对象，打开游标
cur_select.arraysize = 5000
cur_insert.arraysize = 5000
source_table = input("请输入源表名称:")  # 从键盘获取源表名称
target_table = input("请输入目标表名称:")  # 从键盘获取目标表名称
select_sql = 'select * from ' + source_table  # 源查询SQL，如果有where过滤条件，在这里拼接
cur_select.execute(select_sql)  # 执行
print('开始执行:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
while True:
    rows = cur_select.fetchmany(5000)  # 每次获取5000行，由cur_select.arraysize值决定
    data = pd.DataFrame(rows)
    output = StringIO()
    data.to_csv(output, sep='\t', index=False, header=False)
    output1 = output.getvalue()
    cur_insert.copy_from(StringIO(output1), target_table, sep='\t', null='')
    target_db.commit()
    if not rows:
        break  # 中断循环
cur_select.close()
cur_insert.close()
source_db.close()
target_db.close()
print('执行成功:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))