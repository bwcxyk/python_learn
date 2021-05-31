#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/28 9:20
@Author  : YaoKun
@Usage   : pdf2word 
"""

import os
from pdf2docx import Converter
os.chdir(r'E:\pdf2docx')
cwd = os.getcwd()
items = os.listdir(cwd)

for i in items:
    # print("--i--", i)
    f = os.path.splitext(i)[0]
    # print("----f----", f)
    docx_file = f+'.docx'
    print(docx_file)
    # pdf_file = 'E:/pdf2word/rBOz8WBe5taAFctjAAN55a9hdUg980.pdf'
    # docx_file = 'E:/pdf2word/rBOz8WBe5taAFctjAAN55a9hdUg980.docx'
    # # convert pdf to docx
    cv = Converter(i)
    cv.convert(docx_file, start=0, end=None)
    cv.close()
