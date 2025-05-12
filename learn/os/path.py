#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/23 14:23
@Author  : YaoKun
@Usage   : python path
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("-----BASE_DIR------")
print(f"{BASE_DIR}")
PROJECT_DIR = os.path.dirname(BASE_DIR)
print("-----PROJECT_DIR------")
print(f"{PROJECT_DIR}")
XPACK_DIR = os.path.join(BASE_DIR, 'xpack')
print("-----XPACK_DIR------")
print(f"{XPACK_DIR}")
HAS_XPACK = os.path.isdir(XPACK_DIR)
print("-----HAS_XPACK------")
print(f"{HAS_XPACK}")

# format
parts = ['key', 'value']
targets = ['auth_openid']
for part in parts:
    for target in targets:
        method_name = 'compatible_{}_of_{}'.format(target, part)
        print(f"{method_name}")
