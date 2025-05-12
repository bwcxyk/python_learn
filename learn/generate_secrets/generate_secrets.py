#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/6 11:24
@Author  : YaoKun
@Usage   : python generate_secrets
"""

import secrets
import string

characters = string.ascii_letters + string.digits
secure_password = "".join(secrets.choice(characters) for i in range(10))
print(secure_password)
