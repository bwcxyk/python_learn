#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'YaoKun'
__time__ = '2020/7/13 15:47'

import cx_Oracle
from pprint import pprint
from sys import modules
def main():
    # 建立连接
    #db = cx_Oracle.connect('tms_user_1', 'tms_uat_pwd', '192.168.1.181:1521/orcl')
    #db1 = cx_Oracle.connect('tms_user_1/tms_uat_pwd@192.168.1.181:1521/orcl')
    connection = cx_Oracle.connect('tms_user_1/tms_uat_pwd@192.168.1.181/orcl')

    # 创建游标
    cursor = connection.cursor()

    # 执行sql 语句
    sql = "select max(to_number(RESOURCE_ID)) from SYSTEM_RESOURCE"
    r = cursor.execute(sql)

    # 4.获取数据
    # 获取单个字节组
    row = cursor.fetchone()
    print(row,type(row))
    row_str=''.join('%s' %id for id in row)
    print(row_str,type(row_str))
    row_int=int(row_str)
    print(row_int,type(row_int))
    next_id=row_int+1
    print(next_id,type(next_id))
    # next_id=1000100311
    sql2 = "select * from SYSTEM_RESOURCE where RESOURCE_ID={}"
    sql3 = sql2.format(next_id)
    print(sql3)
    rr = cursor.execute(sql3)

    # 4.获取数据
    # 获取单个字节组
    row1 = cursor.fetchone()
    # 获取所有
    # row = cursor.fetchall()
    # 取10条记录信息
    # row1 = cursor.fetchmany(10)
    print(row1)

    # 关闭游标
    cursor.close()

    # 关闭连接
    connection.close()

if __name__ == '__main__':
    main()