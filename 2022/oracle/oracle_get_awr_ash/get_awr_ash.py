#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2022/9/8 10:00
@Author  : YaoKun
@Usage   : python oracle_awr
"""

# 读取配置文件，请一定要配置好哦，具体的配置说明请看 run_config_template.py 文件的说明
from run_config import oracle_connect_string, oracle_connect_string2, save_folder
from run_config import dbid, instance_number, awr_ash_timepoint, generate_awr, generate_ash
import oracledb
oracledb.init_oracle_client(lib_dir=r"D:\Program Files\instantclient_19_3")


def oracle_connect(connect_string: str):
    conn = oracledb.connect(connect_string)
    cursor = conn.cursor()
    return conn, cursor


# 关闭数据库连接的函数
def oracle_close(cursor, conn):
    cursor.close()
    conn.close()


def get_snap_id(cursor, dbid, time):
    sql = '''select min(a.snap_id) as snap_id from dba_hist_snapshot a
         where a.dbid = :dbid 
         and a.end_interval_time >= to_timestamp(:time, 'yyyy-mm-dd hh24:mi:ss')'''

    cursor.execute(sql, {"dbid": dbid, "time": time})
    row = cursor.fetchone()
    if not row or len(row) != 1:
        raise ValueError(f"Failed to retrieve snapshot ID for time {time}")
    return row[0]


#  将时间格式化
def time_format(time_string: str):
    return time_string.replace("-", "").replace(":", "").replace(" ", "")


# 保存 HTML 文件的函数
def save_html_file(content: str, save_type: str, start_time: str, end_time: str, this_instance_number: int, save_folder: str):
    filename = f"[{save_type} 报告]{time_format(start_time)}到{time_format(end_time)}节点{this_instance_number}.html"
    with open(save_folder + filename, "w", encoding="utf-8") as f:
        for this_row in content:
            if this_row[0] is not None:
                f.write(this_row[0])
            f.write("\n")
    print(f"[{save_type} 报告]【{save_folder}{filename}】已导出成功！")


# 获取 AWR 报告的函数
def get_awr(cursor, awr_ash_timepoint, dbid, instance_number, save_folder):
    for start_time, end_time in awr_ash_timepoint:
        print(f"开始获取 AWR 报告，开始时间：{start_time}，结束时间：{end_time}")
        try:
            start_snap_id = get_snap_id(cursor, dbid, start_time)
            end_snap_id = get_snap_id(cursor, dbid, end_time)
        except Exception as e:
            print(f"Error retrieving snapshot ID: {e}")
            continue

        for instance_num in instance_number:
            sql = f'''select * from table(dbms_workload_repository.awr_report_html({dbid},{instance_num},{start_snap_id},{end_snap_id}))'''
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                save_html_file(rows, 'awr', start_time, end_time, instance_num, save_folder)
            except Exception as e:
                print(f"Error executing AWR report query: {e}")
                continue


# 获取 ASH 报告的函数
def get_ash(cursor, awr_ash_timepoint, dbid, instance_number, save_folder):
    for start_time, end_time in awr_ash_timepoint:
        try:
            for instance_num in instance_number:
                sql = f'''select * from table(dbms_workload_repository.ash_report_html(
                            l_inst_num => {instance_num},
                            l_dbid => {dbid},
                            l_btime => to_date('{start_time}:00','yyyy-mm-dd hh24:mi:ss'),
                            l_etime => to_date('{end_time}:00','yyyy-mm-dd hh24:mi:ss')
                        ))'''
                cursor.execute(sql)
                rows = cursor.fetchall()
                save_html_file(rows, 'ash', start_time, end_time, instance_num, save_folder)
        except Exception as e:
            print(f"Error retrieving ASH report: {e}")
            continue


if __name__ == "__main__":
    # 连接数据库
    conn, cursor = oracle_connect(oracle_connect_string)

    # 获取快照并保存到指定文件夹
    if generate_awr:
        print("正在获取 AWR 报告中...")
        get_awr(cursor, awr_ash_timepoint, dbid, instance_number, save_folder)
    if generate_ash:
        print("正在获取 ASH 报告中...")
        get_ash(cursor, awr_ash_timepoint, dbid, instance_number, save_folder)

    # 关闭数据库连接
    oracle_close(cursor, conn)

    # 当多节点的时候获取 ASH 报告才需要运行
    if generate_ash is True and len(instance_number) > 1 and oracle_connect_string2 != "":
        oracle_connect(oracle_connect_string2)
        print("正在获取 ASH 报告中...")
        get_ash(cursor, awr_ash_timepoint, dbid, instance_number, save_folder)
        oracle_close(cursor, conn)

    print("全部执行完毕！")
