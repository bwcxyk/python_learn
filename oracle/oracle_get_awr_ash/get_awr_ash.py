#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2022/9/8 10:00
@Author  : YaoKun
@Usage   : python oracle_awr
"""

import traceback

import oracledb

# 读取配置文件，请一定要配置好哦，具体的配置说明请看 run_config_template.py 文件的说明
from run_config import oracle_connect_string, oracle_connect_string2, save_folder
from run_config import dbid, instance_number, awr_ash_timepoint, generate_awr, generate_ash


# 初始化 Oracle Client
oracledb.init_oracle_client(
    lib_dir=r"D:\Program Files\instantclient_23_9"
)


def oracle_connect(connect_string: str):
    """
    创建 Oracle 数据库连接
    """
    conn = oracledb.connect(connect_string)
    cursor = conn.cursor()

    # 解决 Oracle 11.2.0.4 生成 ASH 报告时的 ORA-01843
    cursor.execute("""
        ALTER SESSION SET NLS_DATE_LANGUAGE = 'AMERICAN'
    """)

    return conn, cursor


# 关闭数据库连接的函数
def oracle_close(cursor, conn):
    """
    关闭数据库连接
    """
    if cursor:
        cursor.close()

    if conn:
        conn.close()


def get_snap_id(cursor, dbid, time):
    """
    根据时间获取 Snapshot ID
    """
    sql = """
        SELECT MIN(a.snap_id) AS snap_id
        FROM dba_hist_snapshot a
        WHERE a.dbid = :dbid
          AND a.end_interval_time >= TO_TIMESTAMP(
              :time,
              'yyyy-mm-dd hh24:mi:ss'
          )
    """

    cursor.execute(
        sql,
        {
            "dbid": dbid,
            "time": time,
        }
    )

    row = cursor.fetchone()

    if not row or len(row) != 1 or row[0] is None:
        raise ValueError(
            f"Failed to retrieve snapshot ID for time {time}, dbid={dbid}"
        )

    return row[0]


# 将时间格式化
def time_format(time_string: str):
    return time_string.replace("-", "").replace(":", "").replace(" ", "")


# 保存 HTML 文件的函数
def save_html_file(
    content,
    save_type: str,
    start_time: str,
    end_time: str,
    this_instance_number: int,
    save_folder: str
):
    filename = (
        f"[{save_type} 报告]"
        f"{time_format(start_time)}到{time_format(end_time)}"
        f"节点{this_instance_number}.html"
    )

    with open(
        save_folder + filename,
        "w",
        encoding="utf-8"
    ) as f:
        for this_row in content:
            if this_row[0] is not None:
                f.write(this_row[0])
            f.write("\n")

    print(
        f"[{save_type} 报告]"
        f"【{save_folder}{filename}】已导出成功！"
    )


# 获取 AWR 报告的函数
def get_awr(
    cursor,
    awr_ash_timepoint,
    dbid,
    instance_number,
    save_folder
):
    # AWR SQL 使用绑定变量
    sql = """
        SELECT *
        FROM TABLE(
            dbms_workload_repository.awr_report_html(
                :dbid,
                :instance_num,
                :start_snap_id,
                :end_snap_id
            )
        )
    """

    for start_time, end_time in awr_ash_timepoint:
        print(
            f"开始获取 AWR 报告，"
            f"开始时间：{start_time}，"
            f"结束时间：{end_time}"
        )

        try:
            # 获取开始时间对应的 Snapshot ID
            start_snap_id = get_snap_id(
                cursor,
                dbid,
                start_time
            )

            # 获取结束时间对应的 Snapshot ID
            end_snap_id = get_snap_id(
                cursor,
                dbid,
                end_time
            )

            print(
                f"AWR Snapshot ID："
                f"start_snap_id={start_snap_id}，"
                f"end_snap_id={end_snap_id}"
            )

        except Exception as e:
            print(
                f"Error retrieving snapshot ID: {e}"
            )

            # 输出完整异常堆栈
            traceback.print_exc()

            continue

        for instance_num in instance_number:
            try:
                print(
                    f"正在获取 AWR 报告，"
                    f"DBID：{dbid}，"
                    f"节点：{instance_num}"
                )

                # 使用绑定变量执行 AWR
                cursor.execute(
                    sql,
                    {
                        "dbid": dbid,
                        "instance_num": instance_num,
                        "start_snap_id": start_snap_id,
                        "end_snap_id": end_snap_id,
                    }
                )

                rows = cursor.fetchall()

                save_html_file(
                    rows,
                    "awr",
                    start_time,
                    end_time,
                    instance_num,
                    save_folder
                )

            except Exception as e:
                print(
                    f"Error executing AWR report query: {e}"
                )

                print(
                    f"错误参数："
                    f"dbid={dbid}，"
                    f"instance_num={instance_num}，"
                    f"start_snap_id={start_snap_id}，"
                    f"end_snap_id={end_snap_id}"
                )

                # 输出完整异常堆栈
                traceback.print_exc()

                continue


# 获取 ASH 报告的函数
def get_ash(
    cursor,
    awr_ash_timepoint,
    dbid,
    instance_number,
    save_folder
):
    # ASH SQL 使用绑定变量
    sql = """
        SELECT *
        FROM TABLE(
            dbms_workload_repository.ash_report_html(
                l_inst_num => :inst_num,
                l_dbid     => :dbid,
                l_btime    => TO_DATE(
                    :btime,
                    'yyyy-mm-dd hh24:mi:ss'
                ),
                l_etime    => TO_DATE(
                    :etime,
                    'yyyy-mm-dd hh24:mi:ss'
                )
            )
        )
    """

    for start_time, end_time in awr_ash_timepoint:
        print(
            f"开始获取 ASH 报告，"
            f"开始时间：{start_time}，"
            f"结束时间：{end_time}"
        )

        for instance_num in instance_number:
            try:
                print(
                    f"正在获取 ASH 报告，"
                    f"DBID：{dbid}，"
                    f"节点：{instance_num}"
                )

                # 使用绑定变量执行 ASH
                cursor.execute(
                    sql,
                    {
                        "inst_num": instance_num,
                        "dbid": dbid,
                        "btime": start_time,
                        "etime": end_time,
                    }
                )

                rows = cursor.fetchall()

                save_html_file(
                    rows,
                    "ash",
                    start_time,
                    end_time,
                    instance_num,
                    save_folder
                )

            except Exception as e:
                print(
                    f"Error retrieving ASH report: {e}"
                )

                print(
                    f"错误参数："
                    f"dbid={dbid}，"
                    f"instance_num={instance_num}，"
                    f"start_time={start_time}，"
                    f"end_time={end_time}"
                )

                # 输出完整异常堆栈
                traceback.print_exc()

                continue


if __name__ == "__main__":

    # ==========================================================
    # 第一个数据库连接
    # ==========================================================
    conn = None
    cursor = None

    try:
        # 连接数据库
        conn, cursor = oracle_connect(
            oracle_connect_string
        )

        # 获取 AWR 报告
        if generate_awr:
            print("正在获取 AWR 报告中...")

            get_awr(
                cursor,
                awr_ash_timepoint,
                dbid,
                instance_number,
                save_folder
            )

        # 获取 ASH 报告
        if generate_ash:
            print("正在获取 ASH 报告中...")

            get_ash(
                cursor,
                awr_ash_timepoint,
                dbid,
                instance_number,
                save_folder
            )

    except Exception:
        print(
            "第一个数据库连接或报告生成过程中发生异常："
        )

        # 输出完整异常堆栈
        traceback.print_exc()

    finally:
        # 关闭第一个数据库连接
        oracle_close(
            cursor,
            conn
        )


    # ==========================================================
    # 第二个数据库连接
    #
    # 当多节点的时候获取 ASH 报告才需要运行
    # ==========================================================
    if (
        generate_ash is True
        and len(instance_number) > 1
        and oracle_connect_string2 != ""
    ):
        conn2 = None
        cursor2 = None

        try:
            conn2, cursor2 = oracle_connect(
                oracle_connect_string2
            )

            print(
                "正在获取第二个数据库的 ASH 报告中..."
            )

            get_ash(
                cursor2,
                awr_ash_timepoint,
                dbid,
                instance_number,
                save_folder
            )

        except Exception:
            print(
                "第二个数据库连接或 ASH 报告生成过程中发生异常："
            )

            # 输出完整异常堆栈
            traceback.print_exc()

        finally:
            # 关闭第二个数据库连接
            oracle_close(
                cursor2,
                conn2
            )


    print("执行完毕！")
