#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'YaoKun'
__time__ = '2020/7/13 14:23'

import cx_Oracle
from pprint import pprint
from sys import modules
def main():
    # 建立连接
    #db = cx_Oracle.connect('tms_user_1', 'tms_uat_pwd', '192.168.1.181:1521/orcl')
    #db1 = cx_Oracle.connect('tms_user_1/tms_uat_pwd@192.168.1.181:1521/orcl')
    connection = cx_Oracle.connect('tms_user_1/tms_uat_pwd@192.168.1.181/orcl')
    print(connection.version)

    # 创建游标
    cursor = connection.cursor()

    # try:
    #     # 解析sql语句
    #     cursor.parse("select *  dual")
    #     # 捕获SQL异常
    # except cx_Oracle.DatabaseError as e:
    #     print(e)  # ORA-00923: 未找到要求的 FROM 关键字

    # 执行sql 语句
    sql = "select RESOURCE_ID from SYSTEM_RESOURCE where syscode='1000' and name ='用户管理'"
    r = cursor.execute(sql)

    # 4.获取数据
    # 获取单个字节组
    # row = cursor.fetchone()
    # 获取所有
    # row = cursor.fetchall()
    # 取10条记录信息
    row = cursor.fetchmany(10)
    print(row)
    # pprint(row)

    # 关闭游标
    cursor.close()

    # 关闭连接
    connection.close()

if __name__ == '__main__':
    main()