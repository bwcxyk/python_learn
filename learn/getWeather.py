#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'YaoKun'
__time__ = '2019/11/15 15:05'

import requests

def getWeather():
    # 设置心知天气的apikey
    # 并构造请求URL
    xinzhi_apikey = "SegOxxxfd5_OWKT"
    url = "https://api.seniverse.com/v3/weather/now.json" % xinzhi_apikey

    # 获取天气预报信息
    # 此处只取今天和明天2天的预报
    r = requests.get(url)
    w = r.json()["results"][0]["daily"]
    today = "今天是%s，白天%s，晚上%s，最高气温%s，最低气温%s" % (w[0]["date"], w[0]["text_day"], w[0]["text_night"], w[0]["high"], w[0]["low"])
    tomorrow = "明天是%s，白天%s，晚上%s，最高气温%s，最低气温%s" % (w[1]["date"], w[1]["text_day"], w[1]["text_night"], w[1]["high"], w[1]["low"])
    message = today + '\n' + tomorrow
    print(today)
    #return message