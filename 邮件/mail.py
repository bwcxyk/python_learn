#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText


# 第三方
mail_host = 'smtp.163.com'  # 腾讯smtp服务器
mail_user = 'yaokun_130@163.com'    # 需要登录的邮箱账号
mail_pass = '147369abc'                    # 对应邮箱密码也就是授权码,需要开启smtp 并启用授权码,代码后面会有提示

message = MIMEText('第一封邮件发送', 'plain', 'utf-8')  # 邮件内容

senderOne = 'yaokun_130@163.com'  # 发件人邮箱(mail_user = 'xx@qq.com')
receiversOne = ['1624717079@qq.com', 'yaokun_130@163.com','2237553939@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
message['From'] = "{}".format(senderOne)
message['To'] = ",".join(receiversOne)

title = '测试邮件'
message['Subject'] = title


try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)  # 登录验证
    smtpObj.sendmail(senderOne, receiversOne, message.as_string())  # 发送
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")