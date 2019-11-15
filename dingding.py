#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import sys
import os

headers = {'Content-Type': 'application/json;charset=utf-8'}
api_url = "https://oapi.dingtalk.com/robot/send?access_token=这里填写自己钉钉群自定义机器人的token"
#需要更换你机器人的地址
def msg(text):
    json_text= {
     "msgtype": "text",
     "text": {
         "content": text
     },
     "at": {
         "atMobiles": [
             "186..." #需要@群里谁
         ],
         "isAtAll": True #是否全部@，True为是,False为否
     }
    }
    print requests.post(api_url,json.dumps(json_text),headers=headers).content

if __name__ == '__main__':
    text = sys.argv[1]
    msg(text)
