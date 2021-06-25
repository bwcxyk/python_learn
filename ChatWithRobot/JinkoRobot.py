#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Jinko Robot
import json
import urllib.request
import urllib.parse


class JinkoRobot:
    __answer = ''

    def __init__(self):
        pass

    # 倾听话语
    def listenFor(self, string):
        self.__answer = self.thinking(string)

    # 思考着
    def thinking(self, string):
        says = urllib.parse.quote_plus(string)
        f = urllib.request.urlopen(
            "http://www.tuling123.com/openapi/api?key=4bc32d41c10be18627438ae45eb839ac&info=" + says)
        json_str = f.read()
        thinkdata = json.loads(json_str.decode('utf-8'))
        f.close()

        if 40000 < thinkdata['code'] < 40010:
            return "今天张三被你问得有点累了, 过会再问吧!"

        if thinkdata['code'] == 200000:
            return thinkdata['text'] + ", 猛戳这里>>" + thinkdata['url']

        if thinkdata['code'] == 302000:
            info = thinkdata['text']

            for content in thinkdata['list']:
                info += "\n\n>" + content['article'] \
                        + "  来源于" + content['source'] \
                        + "  详细信息请猛戳这里>>" + content['detailurl']

            return info

        if thinkdata['code'] == 305000:
            info = thinkdata['text']

            for key in thinkdata['list']:
                info += "\n\n>" + key + ": 车次>" + content['trainnum'] \
                        + "  从" + content['start'] + "到" + content['terminal'] \
                        + "  发车时间:" + content['starttime'] \
                        + "  到达时间:" + content['endtime'] \
                        + "  详细信息请猛戳这里>>" + content['detailurl']

            return info

        return thinkdata['text']

    # 和你交流回答
    def answer(self):
        return self.__answer
