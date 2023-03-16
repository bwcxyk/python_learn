#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/2/27 9:32
@Author  : YaoKun
@Usage   : python escape.py
"""

filter_table = """
"IN('TMS_ORDER_SHIP_B0923','OMS_TO_TMS_LOG','TMS_REPORT_INCOME_COST2','TMS_TRANS_TRANSPORT_PD_221226')\"
"""


def add_escape(value):
    reserved_chars = r'''?&|!{}[]()^~*:\\"'+- '''
    replace = ['\\' + l for l in reserved_chars]
    trans = str.maketrans(dict(zip(reserved_chars, replace)))
    return value.translate(trans)


filter_table = add_escape(filter_table)
print(filter_table)
