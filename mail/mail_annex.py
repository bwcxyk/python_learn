#!/usr/bin/python3

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# 第三方邮件服务器设置
mail_host = 'smtp.163.com'  # smtp服务器
mail_user = '***@163.com'   # 需要登录的邮箱账号
mail_pass = '***'           # 邮箱密码或者授权码,需要开启smtp

#内容项
sender = 'yaokun_130@163.com'           # 发件人邮箱(mail_user = 'xx@qq.com')
receivers = ['yaokun_130@163.com','2237553939@qq.com']  # 接收邮箱，可设置QQ邮箱或者其他邮箱
subject = 'Python SMTP 邮件发送测试'     #主题
message = MIMEMultipart()

message.attach(MIMEText('这是Python 邮件发送测试……', 'plain', 'utf-8'))
message['From'] = "{}".format(sender)
message['To'] = ",".join(receivers)
message['Subject'] = Header(subject, 'utf-8')

# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="test.txt"'
message.attach(att1)

# 构造附件2，传送当前目录下的 runoob.txt 文件
att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')
att2["Content-Type"] = 'application/octet-stream'
att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
message.attach(att2)

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)         # 登录验证
    smtpObj.sendmail(sender, receivers, message.as_string())    # 发送
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")