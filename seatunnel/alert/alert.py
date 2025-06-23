#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/6/23 上午11:04
@Author  : YaoKun
@Usage   : python alert.py
"""
import os
import requests
import json
import time
import hmac
import hashlib
import base64
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 加载环境变量
load_dotenv()

# 配置常量
SERVER_URL = os.getenv("SERVER_URL")
DINGTALK_TOKEN = os.getenv('DINGTALK_TOKEN')
DINGTALK_SECRET = os.getenv('DINGTALK_SECRET', '')  # 默认为空字符串
MONITOR_WINDOW_MINUTES = int(os.getenv('MONITOR_WINDOW_MINUTES', 15))  # 默认15分钟
REQUEST_TIMEOUT = 10  # 请求超时时间(秒)


def is_recent_failure(finish_time_str: str, window_minutes: int) -> bool:
    """
    检查任务是否在最近指定时间内完成
    :param finish_time_str: 完成时间字符串，格式"YYYY-MM-DD HH:MM:SS"
    :param window_minutes: 监控时间窗口(分钟)
    :return: 是否在时间窗口内
    """
    if not finish_time_str or window_minutes <= 0:
        return False

    try:
        finish_time = datetime.strptime(finish_time_str, "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - finish_time) <= timedelta(minutes=window_minutes)
    except (ValueError, TypeError) as e:
        print(f"[WARN] 时间解析错误: {str(e)} | 时间字符串: '{finish_time_str}'")
        return False


def build_dingtalk_webhook() -> str:
    """
    构建钉钉webhook URL
    :return: 完整的webhook URL
    """
    base_url = f"https://oapi.dingtalk.com/robot/send?access_token={DINGTALK_TOKEN}"

    if not DINGTALK_SECRET:
        return base_url

    timestamp = str(round(time.time() * 1000))
    sign = base64.b64encode(
        hmac.new(
            DINGTALK_SECRET.encode('utf-8'),
            f"{timestamp}\n{DINGTALK_SECRET}".encode('utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8')

    return f"{base_url}&timestamp={timestamp}&sign={sign}"


def send_dingtalk_alert(job_info: dict) -> dict:
    """
    发送钉钉告警消息
    :param job_info: 任务信息字典
    :return: 钉钉API响应
    """
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "SeaTunnel-任务失败告警",
            "text": (
                "### 任务失败告警\n\n"
                f"- **地址**: {SERVER_URL}\n"
                f"- **任务ID**: {job_info.get('jobId', 'N/A')}\n"
                f"- **任务名称**: {job_info.get('jobName', 'N/A')}\n"
                f"- **状态**: {job_info.get('jobStatus', 'N/A')}\n"
                f"- **创建时间**: {job_info.get('createTime', 'N/A')}\n"
                f"- **完成时间**: {job_info.get('finishTime', 'N/A')}\n\n"
                "请及时处理！"
            )
        }
    }

    try:
        response = requests.post(
            build_dingtalk_webhook(),
            headers={"Content-Type": "application/json"},
            data=json.dumps(message),
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 钉钉消息发送失败: {str(e)}")
        return {"error": str(e)}


def check_failed_jobs():
    """检查失败任务并发送告警"""
    print(f"开始检查失败任务，时间窗口: 最近 {MONITOR_WINDOW_MINUTES} 分钟...")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # 获取任务数据
        response = requests.get(SERVER_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        jobs = response.json()

        recent_failures = 0
        for job in jobs:
            job_info = {
                "jobId": job.get("jobId", ""),
                "jobName": job.get("jobName", ""),
                "jobStatus": job.get("jobStatus", ""),
                "createTime": job.get("createTime", ""),
                "finishTime": job.get("finishTime", "")
            }

            # 检查失败任务
            if (job_info["jobStatus"] == "FAILED" and
                    is_recent_failure(job_info["finishTime"], MONITOR_WINDOW_MINUTES)):
                print(f"[ALERT] 发现失败任务: ID={job_info['jobId']}, 名称={job_info['jobName']}")
                send_dingtalk_alert(job_info)
                recent_failures += 1

        print(f"检查完成，共发现{recent_failures}个近期失败任务 (当前时间: {current_time})")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 请求接口失败: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"[ERROR] 响应数据解析失败: {str(e)}")
    except Exception as e:
        print(f"[ERROR] 未知错误: {str(e)}")


if __name__ == "__main__":
    check_failed_jobs()
