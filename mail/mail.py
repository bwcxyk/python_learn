#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText

# 第三方邮件服务器设置
mail_host = 'smtp.163.com'  # smtp服务器
mail_user = '***@163.com'   # 需要登录的邮箱账号
mail_pass = '***'           # 邮箱密码或者授权码,需要开启smtp

#内容项，下面有引用
senderOne = 'yaokun_130@163.com'     # 发件人邮箱(mail_user = 'xx@qq.com')
receiversOne = ['yaokun_130@163.com','2237553939@qq.com']  # 接收邮箱，可设置QQ邮箱或者其他邮箱
subject = 'Python SMTP 邮件发送测试'  # 邮件主题

message['Subject'] = subject              # 主题
message = MIMEText('第一封邮件发送', 'plain', 'utf-8')  # 内容
message['From'] = "{}".format(senderOne)  # 发送者
message['To'] = ",".join(receiversOne)    # 接收者

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)         # 登录验证
    smtpObj.sendmail(senderOne, receiversOne, message.as_string())  # 发送
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")