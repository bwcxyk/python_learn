#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/6 11:13
@Author  : YaoKun
@Usage   : python generate_hash
"""

import hashlib
from random import Random


def random_str():
    randomlength = 6
    str = ''
    #    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    chars = 'abcdefghijklmnopqrstuvwxyz0123456'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


hash = open("hash.txt", "w+")
plain_hash = open("plain_hash.txt", "w+")

num = 10000
i = 0
while i < num:
    str = random_str()
    sha1 = hashlib.sha1(str)
    sha1_hex = sha1.hexdigest()
    str = sha1_hex + ":" + str + "\n"
    sha1_hex += "\n"
    plain_hash.write(str)
    hash.write(sha1_hex)
    i += 1
hash.close()
plain_hash.close()
