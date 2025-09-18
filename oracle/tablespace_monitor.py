#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Oracle 表空间监控脚本 - 使用本地认证(sysdba)
当最大剩余空间不足5000MB时发送邮件（HTML格式）
Python 3.6 兼容版
"""
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime

# ================= 配置部分 =================
# 最小剩余空间阈值
MIN_REMAINING_MB = 5000
LOG_FILE = "/var/log/oracle_tablespace_monitor.log"

# 发件人
MAIL_FROM_NAME = "通知"
# 收件人
MAIL_TO = ["1624717079@qq.com"]
# 邮件主题前缀
MAIL_SUBJECT_PREFIX = "Oracle表空间预警通知 - "

# 邮箱配置（SMTP）
SMTP_SERVER = "smtp.feishu.cn"
SMTP_PORT = 465
SMTP_USER = "notice@xxx.com"
SMTP_PASS = "xxx"

# ================= 日志函数 =================
def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = "{} - {}".format(now, msg)
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ================= SQL 查询函数 =================
def get_tablespace_query(min_remaining_mb):
    return """
SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF LINESIZE 1000
WITH ts_stats AS (
    SELECT
        d.tablespace_name tbsname,
        round(d.tablespace_size*(SELECT value FROM v$parameter WHERE name = 'db_block_size')/1024/1024, 2) total_mb,
        round(d.used_space*(SELECT value FROM v$parameter WHERE name = 'db_block_size')/1024/1024, 2) used_mb,
        round((d.tablespace_size-d.used_space)*(SELECT value FROM v$parameter WHERE name = 'db_block_size')/1024/1024, 2) left_mb,
        round(d.used_percent, 2) usage_pct,
        (SELECT MAX(autoextensible) FROM dba_data_files WHERE tablespace_name=d.tablespace_name) autoextensible,
        (SELECT COUNT(file_name) FROM dba_data_files WHERE tablespace_name=d.tablespace_name) count_file
    FROM
        dba_tablespace_usage_metrics d
    WHERE
        d.tablespace_name NOT IN (
            SELECT tablespace_name FROM dba_tablespaces
            WHERE contents = 'TEMPORARY' OR contents = 'UNDO'
        )
)
SELECT
    '<tr><td>' || tbsname || '</td><td>' || total_mb || '</td><td>' ||
    used_mb || '</td><td>' || left_mb || '</td><td>' || usage_pct ||
    '</td><td>' || autoextensible || '</td><td>' || count_file || '</td></tr>'
FROM ts_stats
WHERE left_mb < {0}
ORDER BY total_mb DESC;
""".format(min_remaining_mb)

def execute_sql_query(sql_query):
    try:
        # 在 CentOS7 Python3.6 下兼容写法
        # linux定时任务
        # . /home/oracle/.bash_profile; /usr/bin/python3 script.py
        cmd = 'sqlplus -s / as sysdba'
        result = subprocess.run(
            cmd,
            input=sql_query.encode("utf-8"),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        output = result.stdout.decode("utf-8").strip()
        err = result.stderr.decode("utf-8").strip()
        if err:
            log("SQL stderr: {}".format(err))
        if "ORA-" in output or "SP2-" in output:
            log("SQL执行错误: {}".format(output))
            return None
        return output
    except subprocess.CalledProcessError as e:
        log("SQL执行异常: {}".format(e))
        return None

# ================= 发送 HTML 邮件 =================
def send_html_email(message_rows):
    if not message_rows:
        log("没有需要发送的表空间告警邮件")
        return

    html_content = """
    <html>
    <head><meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; }}
        h1 {{ color: #d9534f; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
    </head>
    <body>
        <h1>Oracle 表空间预警通知</h1>
        <p>以下表空间最大剩余空间不足 <b>{0}MB</b>，请及时处理！</p>
        <table>
            <tr>
                <th>表空间名</th>
                <th>总大小(MB)</th>
                <th>已使用空间(MB)</th>
                <th>剩余空间(MB)</th>
                <th>使用率(%)</th>
                <th>自动扩展</th>
                <th>数据文件数</th>
            </tr>
            {1}
        </table>
        <p><small>监控服务器: {2}<br>报告时间: {3}</small></p>
    </body>
    </html>
    """.format(MIN_REMAINING_MB,
               message_rows,
               subprocess.getoutput('hostname -I').split()[0],
               datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    try:
        msg = MIMEText(html_content, "html", "utf-8")
        msg["From"] = formataddr((MAIL_FROM_NAME, SMTP_USER))
        msg["To"] = ",".join(MAIL_TO)
        hostname_ip = subprocess.getoutput('hostname -I').split()[0]
        msg["Subject"] = MAIL_SUBJECT_PREFIX + hostname_ip

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, MAIL_TO, msg.as_string())
        log("HTML 邮件发送成功")
    except Exception as e:
        log("邮件发送失败: {}".format(e))

# ================= 主函数 =================
def main():
    # 清空日志文件
    open(LOG_FILE, "w").close()

    log("开始执行Oracle表空间监控检查")
    sql_query = get_tablespace_query(MIN_REMAINING_MB)
    result = execute_sql_query(sql_query)
    if result:
        log("检测到表空间不足情况")
        send_html_email(result)
    else:
        log("表空间状态正常")
    log("监控检查完成")

if __name__ == "__main__":
    main()
