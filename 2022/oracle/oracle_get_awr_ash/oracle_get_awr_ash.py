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
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"D:\Program Files\instantclient_19_3")

global conn
global cursor


def oracle_connect(connect_string: str):
    """连接 oracle"""
    global conn
    global cursor
    conn = cx_Oracle.connect(connect_string)
    cursor = conn.cursor()


def oracle_close():
    """关闭 oracle 连接"""
    cursor.close()
    conn.close()


def exec_create_snapshot():
    """执行生成快照"""
    func_name = '''dbms_workload_repository.create_snapshot'''
    try:
        # 执行调用 function，若为 procedure，则使用 callproc 命令
        # 参考资料：https://www.oracle.com/technetwork/cn/tutorials/python-155134-zhs.html
        res = cursor.callfunc(func_name, cx_Oracle.NUMBER, ('TYPICAL',))
        print("执行生成快照成功！生成的最新快照 ID：%s" % int(res))
    except Exception as e:
        print("执行生成快照报错，报错内容：%s" % e)


def time_format(time_string: str):
    """将时间格式化"""
    return time_string.replace("-", "").replace(":", "").replace(" ", "")


def get_awr():
    """获取 AWR 报告并保存到指定文件夹"""
    for i in awr_ash_timepoint:
        # print(i)
        # 获取起止点的 snap_id
        your_time = "your_time"
        # sql 语句结尾不要有分号~
  #       sql = f'''select distinct(a.snap_id) as snap_id
  # from dba_hist_snapshot a
  # where a.dbid = {dbid}
  #   and extract(day from (a.end_interval_time - to_timestamp('{your_time}', 'yyyy-mm-dd hh24:mi'))) * 86400 +
  #   extract(hour from (a.end_interval_time - to_timestamp('{your_time}', 'yyyy-mm-dd hh24:mi'))) * 3600 +
  #   extract(minute from (a.end_interval_time - to_timestamp('{your_time}', 'yyyy-mm-dd hh24:mi'))) * 60 +
  #   extract(second from (a.end_interval_time - to_timestamp('{your_time}', 'yyyy-mm-dd hh24:mi'))) < 60
  #   and extract(day from (a.end_interval_time - to_timestamp('{your_time}', 'yyyy-mm-dd hh24:mi'))) * 86400 +
  #   extract(hour from (a.end_interval_time - to_timestamp('{your_time}', 'yyyy-mm-dd hh24:mi'))) * 3600 +
  #   extract(minute from (a.end_interval_time - to_timestamp('{your_time}', 'yyyy-mm-dd hh24:mi'))) * 60 +
  #   extract(second from (a.end_interval_time - to_timestamp('{your_time}', 'yyyy-mm-dd hh24:mi'))) >= 0
  #       '''
        sql = f'''select min(a.snap_id) as snap_id from dba_hist_snapshot a
        where a.dbid = {dbid} 
        and a.end_interval_time>=to_date('{your_time}','yyyy-mm-dd hh24:mi')
        '''
        start_sql = sql.replace("your_time", i[0])
        end_sql = sql.replace("your_time", i[1])
        # print(start_sql, "\n", end_sql)
        try:
            cursor.execute(start_sql)
        except Exception as e:
            print("获取开始时点 id 报错，对应时间为【%s】，报错内容：%s" % (i[0], e))
        row = cursor.fetchall()
        if len(row) != 1:
            print("获取开始时点 id 报错，对应时间为【%s】，数量不唯一，结果为【%s】" % (i[0], row))
            continue
        start_snap_id = row[0][0]
        try:
            cursor.execute(end_sql)
        except Exception as e:
            print("获取结束时点 id 报错，对应时间为【%s】，报错内容：%s" % (i[1], e))
        row = cursor.fetchall()
        if len(row) != 1:
            print("获取结束时点 id 报错，对应时间为【%s】，数量不唯一，结果为【%s】" % (i[1], row))
            continue
        end_snap_id = row[0][0]
        for j in instance_number:
            sql = f'''select * from table(dbms_workload_repository.awr_report_html({dbid},{j},{start_snap_id},{end_snap_id}))'''
            try:
                cursor.execute(sql)
            except Exception:
                print("获取 AWR 报告失败，执行语句为【%s】，不做后续保存操作" % sql)
                continue
            row = cursor.fetchall()
            save_html_file(row, 'awr', i[0], i[1], j)


def get_ash():
    """获取 ASH 报告并保存到指定文件夹"""
    for i in awr_ash_timepoint:
        start_time = i[0]
        end_time = i[1]
        for j in instance_number:
            sql = f'''select * from table(dbms_workload_repository.ash_report_html(l_inst_num => {j},
                                l_dbid => {dbid},
                                l_btime => to_date('{start_time}:00','yyyy-mm-dd hh24:mi:ss'),
                                l_etime =>to_date('{end_time}:00','yyyy-mm-dd hh24:mi:ss')
            ))'''
            try:
                cursor.execute(sql)
            except Exception as e:
                if str(e).find('无效的月份') > -1:
                    # 说明只是这个节点获取不到，换个节点就能获取该报告了
                    print("当前连接节点获取不到对应着别的节点的 ASH 报告，跳过...")
                else:
                    print("获取 ASH 报告失败，执行语句为【%s】，不做后续保存操作" % sql)
                continue
            row = cursor.fetchall()
            save_html_file(row, 'ash', start_time, end_time, j)


def save_html_file(content: str, save_type: str, start_time: str, end_time: str, this_instance_number: int):
    # content 为获取出的 html 内容，供保存使用
    # save_type 为保存的类型，会体现在保存的文件名上
    filename = "[%s 报告]%s到%s节点%s.html" % (save_type, time_format(start_time), time_format(end_time), this_instance_number)
    with open(save_folder + filename, "w", encoding="utf-8") as f:
        for this_row in content:
            if this_row[0] is not None:
                f.write(this_row[0])
            f.write("\n")
    print("[%s 报告]【%s%s】已导出成功！" % (save_type, save_folder, filename))


if __name__ == "__main__":
    # 连接数据库
    oracle_connect(oracle_connect_string)

    # 执行生成快照，如果有定时任务及时生成了快照，此项非必须，会生成当下时点的快照，若无需要，可不启用
    # exec_create_snapshot()

    # 获取快照并保存到指定文件夹
    if generate_awr:
        print("正在获取 AWR 报告中...")
        get_awr()
    if generate_ash:
        print("正在获取 ASH 报告中...")
        get_ash()

    # 关闭数据库连接
    oracle_close()

    # 当多节点的时候获取 ASH 报告才需要运行
    if generate_ash is True and len(instance_number) > 1 and oracle_connect_string2 != "":
        oracle_connect(oracle_connect_string2)
        print("正在获取 ASH 报告中...")
        get_ash()
        oracle_close()

    print("全部执行完毕！")
