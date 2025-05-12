#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/9/13 9:23
@Author  : YaoKun
@Usage   : python ocr
"""

import os
import yaml

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkocr.v1.region.ocr_region import OcrRegion
from huaweicloudsdkocr.v1 import *

# 读取配置文件
def get_yaml_data(yaml_file):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    return data

if __name__ == "__main__":
    current_path = os.path.abspath("../config")
    yaml_path = os.path.join(current_path, "config.yaml")
    config_file = get_yaml_data(yaml_path)
    ak = config_file["huaweiocr"]["AccessKey"]
    sk = config_file["huaweiocr"]["SecretAccessKey"]

    credentials = BasicCredentials(ak, sk) \

    client = OcrClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(OcrRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = RecognizeIdCardRequest()
        request.body = IdCardRequestBody(
            side="front",
            url="https://file.yuanfusc.com/group1/M00/09/B5/rBOz8V25Iu2ACDmCAACQ5EvSOMg247.jpg"
        )
        response = client.recognize_id_card(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)