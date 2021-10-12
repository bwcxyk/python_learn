#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/25 15:04
@Author  : YaoKun
@Usage   : python dingding
"""

import time
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem

token = 'xxxxxxxxxxxxxxx'
# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=' + token
secret = 'xxxxxxxxxxxxxx'  # 可选：创建机器人勾选“加签”选项时使用
# 初始化机器人
xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
# at_mobiles = ['这里填写需要提醒的用户的手机号码，字符串或数字都可以']
at_mobiles = ['+86-188xxxx8062']

# Text消息@所有人
while True:
    message = input("请输出要发送的内容:（输出q或quit退出）")
    print(message)
    if message == 'q' or message == 'quit':
        break
    else:
        xiaoding.send_text(msg=message, at_mobiles=at_mobiles)
        time.sleep(1)
