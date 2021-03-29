#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'Fighter.Kun'
__time__ = '2019/9/6 14:52'

'''
class MyClass:
    """一个简单的类实例"""
    i = 12345

    def f(self):
        return 'hello world'
    def a(self):
        return "what's you name?"
    def c(self):
        return '你好'


# 实例化类
x = MyClass()

# 访问类的属性和方法
print("MyClass 类的属性 i 为：", x.i)
print("MyClass 类的方法 f 输出为：", x.f())
print("MyClass 类的方法 a 输出为：",x.a())
print(x.a(),x.c(),x.f(),x.i)

'''

'''
# 类定义
class people:
    # 定义基本属性
    name = ''
    age = 0
    # 定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0

    # 定义构造方法
    def __init__(self, n, a, w):
        self.name = n
        self.age = a
        self.__weight = w

    def speak(self):
        print("%s说:我%r岁,%r斤。"% (self.name, self.age ,self.__weight))

# 实例化类
p = people('张三', 20, 100)
p.speak()
'''



