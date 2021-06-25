#!/usr/bin/env python
# -*- coding: utf-8 -*-


# tcp server
import socket
# import time
import threading
# from JinkoRobot import *
from ChatWithRobot.JinkoRobot import JinkoRobot


# 应用程序入口类


class ApplicationServer:

    # 构造函数初始化 socket
    def __init__(self, host="localhost", port=8005):
        self.connList = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(100)
        print("我是张三, 我来自[图灵机器人:http://www.tuling123.com]")
        print("")
        print("赶紧打开客户端和我聊天吧!")
        self.accept()

    # 多线程接受用户请求
    def accept(self):
        while True:
            connection, address = self.socket.accept()
            # print('connect')
            thread = ChatThread(connection)
            thread.start()


# 聊天线程
class ChatThread(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.__connection = conn

    def run(self):
        while True:
            try:
                recv = self.__connection.recv(8192)
            except:
                break

            # print("收到:" + recv.decode('utf-8'))
            rebot = JinkoRobot()
            rebot.listenFor(recv.decode('utf-8'))
            answer = rebot.answer()
            # print('say:' + answer)
            self.__connection.send(answer.encode('utf-8'))


ApplicationServer()
