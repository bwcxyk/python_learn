#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/28 9:20
@Author  : YaoKun
@Usage   : python 
"""

import os
from pdf2docx import Converter

cwd = os.getcwd()
items = os.listdir(cwd)

pdf_file = 'E:/pdf2word/rBOz8WBe5taAFctjAAN55a9hdUg980.pdf'
docx_file = 'E:/pdf2word/rBOz8WBe5taAFctjAAN55a9hdUg980.docx'

# convert pdf to docx
cv = Converter(pdf_file)
cv.convert(docx_file, start=0, end=None)
cv.close()
