#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/6/9 14:54
@Author  : YaoKun
@Usage   : python security_group.py
"""

import os
import requests
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest, AuthorizeSecurityGroupRequest
from aliyunsdkecs.request.v20140526.RevokeSecurityGroupRequest import RevokeSecurityGroupRequest
from dotenv import load_dotenv

# 解析 .env 文件中的环境变量
load_dotenv()
access_key = os.getenv("access_key")
access_secret = os.getenv('access_secret')
region_id = os.getenv('region_id')
sg_id = os.getenv('sg_id')

# 连接阿里云
client = AcsClient(access_key, access_secret, region_id)


def update_security_group():
    # 获取当前的公网IP
    ip = requests.get("http://ip.42.pl/raw").text.strip()
    # 需要授权的端口列表
    port_list = [22, 1521, 3306, 5432, 6379]

    # 获取指定的安全组
    sg_request = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
    sg_request.set_SecurityGroupId(sg_id)
    try:
        response = client.do_action_with_exception(sg_request)
        security_group = json.loads(response)['SecurityGroups']['SecurityGroup'][0]
        # 打印安全组的名称
        print(f"Security group: {security_group['SecurityGroupName']}")
    except Exception as e:
        print(f"Failed to get security group with ID '{sg_id}': {e}")
        security_group = None
    # 如果 security_group 为空，则退出程序
    if security_group is None:
        exit()

    # 读取上一次的公网 IP
    if os.path.exists("/data/ip.txt"):
        with open("/data/ip.txt", "r") as f:
            old_ip = f.read().strip()
    else:
        old_ip = ""

    # 如果公网 IP 改变了，删除旧的授权规则
    if ip != old_ip:
        # 遍历需要授权的端口列表，给安全组添加授权规则
        for port in port_list:
            # 删除已有的授权规则
            revoke_request = RevokeSecurityGroupRequest()
            revoke_request.set_SecurityGroupId(sg_id)
            revoke_request.set_IpProtocol('tcp')
            revoke_request.set_PortRange(f'{port}/{port}')
            revoke_request.set_SourceCidrIp(f'{old_ip}/32')
            print(f"删除安全组的规则: port={port}, SourceCidrIp={old_ip}")
            try:
                client.do_action_with_exception(revoke_request)
                print(f"端口{port}删除成功")
            except Exception as e:
                print(f"端口{port}删除失败: {e}")

            # 添加新的授权规则
            authorize_request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
            authorize_request.set_IpProtocol('tcp')
            authorize_request.set_PortRange(f'{port}/{port}')
            authorize_request.set_SourceCidrIp(f'{ip}/32')
            authorize_request.set_SecurityGroupId(sg_id)
            print(f"添加安全组规则：允许来自 IP {ip} 的请求访问端口 {port}")
            try:
                client.do_action_with_exception(authorize_request)
                print(f"端口{port}授权成功")
            except Exception as e:
                print(f"端口{port}授权失败: {e}")

        # 将新的公网 IP 写入文件
        with open("/data/ip.txt", "w") as f:
            f.write(ip)

        print("安全组授权更新成功。")
    else:
        print("公网IP未改变，无需更新安全组授权。")


if __name__ == '__main__':
    update_security_group()
