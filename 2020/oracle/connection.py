#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'YaoKun'
__time__ = '2020/7/13 15:54'

import cx_Oracle
from pprint import pprint
from sys import modules

connection = cx_Oracle.connect('tms_user_1/tms_uat_pwd@192.168.1.181/orcl')
cursor = connection.cursor ()

try:
    # 解析sql语句
    cursor.parse("select *  dual")
    # 捕获SQL异常
except cx_Oracle.DatabaseError as e:
    print(e)   # ORA-00923: 未找到要求的 FROM 关键字

# 执行sql 语句
cursor.execute ("select * from dual")
# 提取一条数据，返回一个元祖
row = cursor.fetchone()
pprint(row)  # ('X',)