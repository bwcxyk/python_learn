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
ip_file = os.getenv('ip_file')
port_list_str = os.getenv('port_list')
port_list = [int(port.strip()) for port in port_list_str.split(',')]

# 连接阿里云
client = AcsClient(access_key, access_secret, region_id)


def get_old_ip():
    if os.path.exists(ip_file):
        with open(ip_file, "r") as file:
            return file.read().strip()
    return ""


def get_current_public_ip():
    return requests.get("https://ip.42.pl/raw").text.strip()


def describe_security_group():
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


def remove_authorization():
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


def add_authorization():
    for port in port_list:
        # 添加新的授权规则
        authorize_request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        authorize_request.set_IpProtocol('tcp')
        authorize_request.set_PortRange(f'{port}/{port}')
        authorize_request.set_SourceCidrIp(f'{new_ip}/32')
        authorize_request.set_SecurityGroupId(sg_id)
        print(f"添加安全组规则：允许来自 IP {new_ip} 的请求访问端口 {port}")
        try:
            client.do_action_with_exception(authorize_request)
            print(f"端口{port}授权成功")
        except Exception as e:
            print(f"端口{port}授权失败: {e}")


if __name__ == '__main__':
    old_ip = get_old_ip()
    new_ip = get_current_public_ip()
    if new_ip != old_ip:
        add_authorization()
        if old_ip:
            remove_authorization()

        # 更新旧IP
        with open(ip_file, "w") as f:
            f.write(new_ip)
            print(f"Updated old IP to {new_ip}")
        print("安全组授权更新成功。")
    else:
        print("公网IP未改变，无需更新安全组授权。")
