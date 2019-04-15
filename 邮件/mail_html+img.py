#!/usr/bin/python3

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


# 第三方邮件服务器设置
mail_host = 'smtp.163.com'          # 腾讯smtp服务器
mail_user = 'yaokun_130@163.com'    # 需要登录的邮箱账号
mail_pass = '147369abc'             # 对应邮箱密码也就是授权码,需要开启smtp 并启用授权码,代码后面会有提示

#内容项，下面有引用
sender = 'yaokun_130@163.com'  # 发件人邮箱(mail_user = 'xx@qq.com')
receivers = ['yaokun_130@163.com','2237553939@qq.com']  # 接收邮箱，可设置QQ邮箱或者其他邮箱
subject = 'Python SMTP 邮件发送测试'  #主题
mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="https://blog.bwcxtech.com">我的博客链接</a></p>
<p>图片演示：</p>
<p><img src="cid:image1"></p>
"""
message = MIMEMultipart('related')
msgAlternative = MIMEMultipart('alternative')

msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
message['Subject'] = Header(subject, 'utf-8')
message['From'] = "{}".format(sender)
message['To'] = ",".join(receivers)
message.attach(msgAlternative)

# 指定图片
fp = open('test.jpg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# 定义图片 ID，在 HTML 文本中引用
msgImage.add_header('Content-ID', '<image1>')
message.attach(msgImage)

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)         # 登录验证
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")