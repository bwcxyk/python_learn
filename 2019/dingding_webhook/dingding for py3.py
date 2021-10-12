#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'YaoKun'
__time__ = '2019/11/15 14:42'

import sys
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem

# WebHook地址
token = '2f55c21xxxxxxxxxxc54748093'
webhook = 'https://oapi.dingtalk.com/robot/send?access_token='+token
secret = 'SEC11b9...这里填写自己的加密设置密钥'  # 可选：创建机器人勾选“加签”选项时使用
# 初始化机器人小丁
# xiaoding = DingtalkChatbot(webhook)  # 方式一：通常初始化方式
xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
# xiaoding = DingtalkChatbot(webhook, pc_slide=True)  # 方式三：设置消息链接在PC端侧边栏打开（v1.5以上新功能）
# at_mobiles = ['这里填写需要提醒的用户的手机号码，字符串或数字都可以']

# Text消息@所有人
xiaoding.send_text(msg='我就是小丁，小丁就是我！', is_at_all=True)

'''
# Text消息之@指定用户
at_mobiles = ['这里填写需要提醒的用户的手机号码，字符串或数字都可以']
xiaoding.send_text(msg='我就是小丁，小丁就是我！', at_mobiles=at_mobiles)

# image表情消息
xiaoding.send_image(pic_url='http://uc-test-manage-00.umlife.net/jenkins/pic/flake8.png')

# Link消息
xiaoding.send_link(title='万万没想到，李小璐竟然...', text='故事是这样子的...',
                   message_url='http://www.kwongwah.com.my/?p=454748", pic_url="https://pbs.twimg.com/media/CEwj7EDWgAE5eIF.jpg')

# Markdown消息@所有人
xiaoding.send_markdown(title='氧气文字', text='#### 广州天气\n'
                                          '> 9度，西北风1级，空气良89，相对温度73%\n\n'
                                          '> ![美景](http://www.sinaimg.cn/dy/slidenews/5_img/2013_28/453_28488_469248.jpg)\n'
                                          '> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n',
                       is_at_all=True)

# Markdown消息@指定用户
xiaoding.send_markdown(title='氧气文字', text='#### 广州天气 @18825166128\n'
                                          '> 9度，西北风1级，空气良89，相对温度73%\n\n'
                                          '> ![美景](http://www.sinaimg.cn/dy/slidenews/5_img/2013_28/453_28488_469248.jpg)\n'
                                          '> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n',
                       at_mobiles=at_mobiles)

# FeedCard消息类型（注意：当发送FeedCard时，pic_url需要传入参数值，必选）
card1 = CardItem(title="氧气美女", url="https://www.dingtalk.com/",
                 pic_url="https://unzippedtv.com/wp-content/uploads/sites/28/2016/02/asian.jpg")
card2 = CardItem(title="氧眼美女", url="https://www.dingtalk.com/",
                 pic_url="https://unzippedtv.com/wp-content/uploads/sites/28/2016/02/asian.jpg")
card3 = CardItem(title="氧神美女", url="https://www.dingtalk.com/",
                 pic_url="https://unzippedtv.com/wp-content/uploads/sites/28/2016/02/asian.jpg")
cards = [card1, card2, card3]
xiaoding.send_feed_card(cards)

# ActionCard整体跳转消息类型
btns1 = [CardItem(title="查看详情", url="https://www.dingtalk.com/")]
actioncard1 = ActionCard(title='万万没想到，竟然...',
                         text='![选择](http://www.songshan.es/wp-content/uploads/2016/01/Yin-Yang.png) \n### 故事是这样子的...',
                         btns=btns1,
                         btn_orientation=1,
                         hide_avatar=1)
xiaoding.send_action_card(actioncard1)
# ActionCard独立跳转消息类型（双选项）
btns2 = [CardItem(title="支持", url="https://www.dingtalk.com/"), CardItem(title="反对", url="https://www.dingtalk.com/")]
actioncard2 = ActionCard(title='万万没想到，竟然...',
                         text='![选择](http://www.songshan.es/wp-content/uploads/2016/01/Yin-Yang.png) \n### 故事是这样子的...',
                         btns=btns2,
                         btn_orientation=1,
                         hide_avatar=1)
xiaoding.send_action_card(actioncard2)

# ActionCard独立跳转消息类型（列表选项）
btns3 = [CardItem(title="支持", url="https://www.dingtalk.com/"), CardItem(title="中立", url="https://www.dingtalk.com/"),
         CardItem(title="反对", url="https://www.dingtalk.com/")]
actioncard3 = ActionCard(title='万万没想到，竟然...',
                         text='![选择](http://www.songshan.es/wp-content/uploads/2016/01/Yin-Yang.png) \n### 故事是这样子的...',
                         btns=btns3,
                         btn_orientation=1,
                         hide_avatar=1)
xiaoding.send_action_card(actioncard3)
'''
