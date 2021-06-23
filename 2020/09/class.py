#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author : yaokun
@Time : 2020/9x9/4 15:03
"""

class test():
    def __init__(self,data=1):
        self.data = data

    def __iter__(self):
        return self
    def __next__(self):
        if self.data > 5:
            raise StopIteration
        else:
            self.data+=1
            return self.data

for item in test(3):
    print(item)