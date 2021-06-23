#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name  :    message.py
   Description:
   Author     :    Deniss.Wang
   date       :    2019/../..
-------------------------------------------------
   Change Activity:
                   2019/../..
-------------------------------------------------
"""

import json
import requests
from conf import config


def send_notification_by_ddRobot(dd_user_mobile='13811166325', out_logs='By Default Value'):
    '''
    :param dd_user_mobile:
    :param out_logs:
    :return:
    '''
    dding_msg = {
        "msgtype": "text",
        "text": {
		    "content":
                out_logs
		},
        "at": {
            "atMobiles": [
                dd_user_mobile
            ],
            "isAtAll": False
        }
    }

    postUrl = "https://oapi.dingtalk.com/robot/send?access_token=%s" % config.dding_robot_token
    dding_msg_json = json.dumps(dding_msg)
    headers = {'content-type': 'application/json'}
    ddRobotPost = requests.post(postUrl, data=dding_msg_json, headers=headers).content


def send_online_msg(out_logs='By Default Value'):
    '''
    :param dd_user_mobile:
    :param out_logs:
    :return:
    '''
    dding_msg = {
        "msgtype": "text",
        "text": {
		    "content":
                out_logs
		}
    }

    postUrl = "https://oapi.dingtalk.com/robot/send?access_token=%s" % config.dding_robot_token
    dding_msg_json = json.dumps(dding_msg)
    headers = {'content-type': 'application/json'}
    ddRobotPost = requests.post(postUrl, data=dding_msg_json, headers=headers).content