#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方邮件服务器设置
mail_host = 'smtp.163.com'  # 腾讯smtp服务器
mail_user = 'yaokun_130@163.com'    # 需要登录的邮箱账号
mail_pass = '147369abc'                    # 对应邮箱密码也就是授权码,需要开启smtp 并启用授权码,代码后面会有提示

sender = 'yaokun_130@163.com'
receivers = ['yaokun_130@163.com','1624717079@qq.com','2237553939@qq.com']

mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="https://blog.bwcxtech.com">这是我的博客</a></p>
"""
message = MIMEText(mail_msg, 'html', 'utf-8')
message['From'] = "{}".format(sender)
message['To'] = ",".join(receivers)

subject = 'Python SMTP 邮件发送测试'
message['Subject'] = Header(subject, 'utf-8')


try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)  # 登录验证
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")