#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/8/4 13:47
@Author  : YaoKun
@Usage   : python DescribeSpotPriceHistory
"""

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
            access_key_id='xxxxx',
            # 您的AccessKey Secret,
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
        describe_spot_price_history_request = ecs_20140526_models.DescribeSpotPriceHistoryRequest(
            network_type='vpc',
            region_id='cn-shanghai',
            instance_type='ecs.t6-c1m4.large'
        )
        response = client.describe_spot_price_history(describe_spot_price_history_request)
        spot_prices = response.body.spot_prices.spot_price_type
        for spot_price_type in spot_prices:
            ConsoleClient.log(f'抢占式实例的实例规格:{spot_price_type.instance_type}')
            ConsoleClient.log(f'抢占式实例是否为I/O优化实例:{spot_price_type.io_optimized}')
            ConsoleClient.log(f'抢占式实例的网络类型:{spot_price_type.network_type}')
            ConsoleClient.log(f'按量付费实例部分原价:{spot_price_type.origin_price}')
            ConsoleClient.log(f'抢占式实例价格:{spot_price_type.spot_price}')
            ConsoleClient.log(f'价格时间:{spot_price_type.timestamp}')
            ConsoleClient.log(f'抢占式实例所属的可用区ID:{spot_price_type.zone_id}')
            ConsoleClient.log(f'-------------------------')

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client('ACCESS_KEY_ID', 'ACCESS_KEY_SECRET')
        describe_spot_price_history_request = ecs_20140526_models.DescribeSpotPriceHistoryRequest(
            network_type='vpc',
            region_id='cn-shanghai',
            instance_type='ecs.t6-c1m4.large'
        )
        response = client.describe_spot_price_history(describe_spot_price_history_request)
        spot_prices = response.body.spot_prices.spot_price_type
        for spot_price_type in spot_prices:
            ConsoleClient.log(f'抢占式实例的实例规格:{spot_price_type.instance_type}')
            ConsoleClient.log(f'抢占式实例是否为I/O优化实例:{spot_price_type.io_optimized}')
            ConsoleClient.log(f'抢占式实例的网络类型:{spot_price_type.network_type}')
            ConsoleClient.log(f'按量付费实例部分原价:{spot_price_type.origin_price}')
            ConsoleClient.log(f'抢占式实例价格:{spot_price_type.spot_price}')
            ConsoleClient.log(f'价格时间:{spot_price_type.timestamp}')
            ConsoleClient.log(f'抢占式实例所属的可用区ID:{spot_price_type.zone_id}')
            ConsoleClient.log(f'-------------------------')


if __name__ == '__main__':
    Sample.main(sys.argv[1:])

