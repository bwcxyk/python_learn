#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/2/27 9:32
@Author  : YaoKun
@Usage   : python escape.py
"""

filter_table = """
"in ('SYS','SYSTEM','SYSMAN','DBSNMP','OUTLN','APPQOSSYS')\"
"""


def add_escape(value):
    reserved_chars = r'''?&|!{}[]()^~*:\\"'+- '''
    replace = ['\\' + l for l in reserved_chars]
    trans = str.maketrans(dict(zip(reserved_chars, replace)))
    return value.translate(trans)


filter_table = add_escape(filter_table)
print(filter_table)
