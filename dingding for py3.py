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

# image表情消息
#xiaoding.send_image(pic_url='http://uc-test-manage-00.umlife.net/jenkins/pic/flake8.png')
# Link消息
#xiaoding.send_link(title='万万没想到，李小璐竟然...', text='故事是这样子的...', message_url='http://www.kwongwah.com.my/?p=454748", pic_url="https://pbs.twimg.com/media/CEwj7EDWgAE5eIF.jpg')
# Markdown消息@所有人
'''
xiaoding.send_markdown(title='氧气文字', text='#### 广州天气\n'
                           '> 9度，西北风1级，空气良89，相对温度73%\n\n'
                           '> ![美景](http://www.sinaimg.cn/dy/slidenews/5_img/2013_28/453_28488_469248.jpg)\n'
                           '> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n',
                           is_at_all=True)
                           '''
# FeedCard消息类型
'''
card1 = CardItem(title="氧气美女", url="https://www.dingtalk.com/", pic_url="https://unzippedtv.com/wp-content/uploads/sites/28/2016/02/asian.jpg")
card2 = CardItem(title="氧眼美女", url="https://www.dingtalk.com/", pic_url="https://unzippedtv.com/wp-content/uploads/sites/28/2016/02/asian.jpg")
card3 = CardItem(title="氧神美女", url="https://www.dingtalk.com/", pic_url="https://unzippedtv.com/wp-content/uploads/sites/28/2016/02/asian.jpg")
cards = [card1, card2, card3]
xiaoding.send_feed_card(cards)
'''
# ActionCard整体跳转消息类型
'''
btns1 = [CardItem(title="查看详情", url="https://www.dingtalk.com/")]
actioncard1 = ActionCard(title='万万没想到，竟然...',
                             text='![选择](http://www.songshan.es/wp-content/uploads/2016/01/Yin-Yang.png) \n### 故事是这样子的...',
                             btns=btns1,
                             btn_orientation=1,
                             hide_avatar=1)
xiaoding.send_action_card(actioncard1)
'''
# ActionCard独立跳转消息类型（双选项）
'''
btns2 = [CardItem(title="支持", url="https://www.dingtalk.com/"), CardItem(title="反对", url="https://www.dingtalk.com/")]
actioncard2 = ActionCard(title='万万没想到，竟然...',
                             text='![选择](http://www.songshan.es/wp-content/uploads/2016/01/Yin-Yang.png) \n### 故事是这样子的...',
                             btns=btns2,
                             btn_orientation=1,
                             hide_avatar=1)
xiaoding.send_action_card(actioncard2)
'''
# ActionCard独立跳转消息类型（列表选项）
'''
btns3 = [CardItem(title="支持", url="https://www.dingtalk.com/"), CardItem(title="中立", url="https://www.dingtalk.com/"), CardItem(title="反对", url="https://www.dingtalk.com/")]
actioncard3 = ActionCard(title='万万没想到，竟然...',
                             text='![选择](http://www.songshan.es/wp-content/uploads/2016/01/Yin-Yang.png) \n### 故事是这样子的...',
                             btns=btns3,
                             btn_orientation=1,
                             hide_avatar=1)
xiaoding.send_action_card(actioncard3)
'''
