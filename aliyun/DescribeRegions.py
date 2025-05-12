# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.

import sys
from typing import List

from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_openapi import models as open_api_models


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Ecs20140526Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            # access_key_id=access_key_id,
            access_key_id='xxxxx',
            # 您的AccessKey Secret,
            # access_key_secret=access_key_secret
            access_key_secret='xxxxx'
        )
        # 访问的域名
        config.endpoint = 'ecs-cn-hangzhou.aliyuncs.com'
        return Ecs20140526Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client('ACCESS_KEY_ID', 'ACCESS_KEY_SECRET')
        describe_regions_request = ecs_20140526_models.DescribeRegionsRequest(
            accept_language='zh-CN',
            resource_type='instance',
            instance_charge_type='PrePaid'
        )
        response = client.describe_regions(describe_regions_request)
        regions = response.body.regions.region
        for region in regions:
            ConsoleClient.log(f'状态:{region.status}')
            ConsoleClient.log(f'地域名称:{region.local_name}')
            ConsoleClient.log(f'地域对应的接入地址:{region.region_endpoint}')
            ConsoleClient.log(f'地域ID:{region.region_id}')
            ConsoleClient.log(f'-------------------------')

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client('ACCESS_KEY_ID', 'ACCESS_KEY_SECRET')
        describe_regions_request = ecs_20140526_models.DescribeRegionsRequest(
            accept_language='zh-CN',
            resource_type='instance',
            instance_charge_type='PrePaid'
        )
        response = client.describe_regions(describe_regions_request)
        regions = response.body.regions.region
        for region in regions:
            ConsoleClient.log(f'状态:{region.status}')
            ConsoleClient.log(f'地域名称:{region.local_name}')
            ConsoleClient.log(f'地域对应的接入地址:{region.region_endpoint}')
            ConsoleClient.log(f'地域ID:{region.region_id}')
            ConsoleClient.log(f'-------------------------')


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
