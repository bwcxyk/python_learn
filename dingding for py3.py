#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'Fighter.Kun'
__time__ = '2019/11/15 14:42'

import sys

from dingtalkchatbot.chatbot import DingtalkChatbot
# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=这里填写自己钉钉群自定义机器人的token'
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook)
# Text消息@所有人
if __name__ == '__main__':
    msg = sys.argv[1]
    xiaoding.send_text(msg=msg, is_at_all=True)
