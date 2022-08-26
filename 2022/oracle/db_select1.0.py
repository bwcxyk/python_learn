#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2022/8/26 15:07
@Author  : YaoKun
@Usage   : python db_select1.0
"""

import cx_Oracle
from openpyxl import load_workbook
import time

start_time = time.time()

cx_Oracle.init_oracle_client(lib_dir=r"D:\Program Files\instantclient_19_3")

# Establish the database connection
connection = cx_Oracle.connect(user="zhangsan", password="123456",
                               dsn="192.168.1.1/orcl")


filename = 'E:/1.xlsx'
wb = load_workbook(filename)
sheet = wb["Sheet1"]
for item in sheet.rows:
    tid = ([item[2].value])
    taskid = ''.join(tid)
    # Obtain a cursor
    cursor = connection.cursor()
    sql = """SELECT TASK_ID,
           REPLACE(OP_PICURL, 'group', 'https://file.yuanfusc.com/group') AS OP_PICURL
    FROM (
             WITH TEMP AS (SELECT ROWNUM ROWNUM1, TASK_ID, OP_PICURL
                           FROM "TMS_APP_TASK_ORDER_DETAIL"
                           WHERE OP_CODE = '004'
                             AND TASK_ID = :taskid)
             SELECT TASK_ID,
                    REGEXP_SUBSTR(OP_PICURL, '[^,]+', 1, LEVEL) OP_PICURL
             FROM TEMP
             CONNECT BY PRIOR ROWNUM1 = ROWNUM1
                    AND LEVEL <= REGEXP_COUNT(OP_PICURL, '[^,]+')
                    AND PRIOR DBMS_RANDOM.VALUE() IS NOT NULL
         )"""
    cursor.execute(sql, taskid=taskid)

    # Loop over the result set
    for row in cursor:
        data = list(row)
        print(data)


end_time = time.time()
print("耗时: {:.2f}秒".format(end_time - start_time))