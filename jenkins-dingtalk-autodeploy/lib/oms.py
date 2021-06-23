#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name  :    *.py
   Description:
   Author     :    Deniss.Wang
   date       :    2019/../..
-------------------------------------------------
   Change Activity:
                   2019/../..
-------------------------------------------------
"""


from conf import config
import jenkins
import time


# 创建jenkins连接
jenkins_server = jenkins.Jenkins(
    config.jenkins_server_url,
    username=config.jenkins_build_user,
    password=config.jenkins_api_token
)


def code_update(job_name='auto_deploy'):
    '''
    :param job_name:
    :return:
    '''
    job_queue_number = jenkins_server.build_job(job_name)
    job_queue_item_info = jenkins_server.get_queue_item(job_queue_number)
    job_executable_result = job_queue_item_info.get('executable')

    if not job_executable_result:

        while True:
            time.sleep(2)
            job_queue_item_info = jenkins_server.get_queue_item(job_queue_number)
            job_executable_result = job_queue_item_info.get('executable')

            if job_executable_result:
                job_executable_number = job_queue_item_info.get('executable').get('number')
                break

    job_build_info = jenkins_server.get_build_info(job_name, job_executable_number)
    job_is_building = job_build_info.get('building')

    if job_is_building is True:

        while True:
            time.sleep(2)
            job_build_info = jenkins_server.get_build_info(job_name, job_executable_number)
            job_is_building = job_build_info.get('building')

            if job_is_building is False:
                break

    job_build_result = job_build_info.get('result')

    return job_build_result,job_executable_number



def get_job_build_log(job_name, job_exec_number):
    '''
    :param job_name:
    :param job_exec_number:
    :return:
    '''
    time.sleep(5)
    out_logs = jenkins_server.get_build_console_output(job_name, job_exec_number)
    list_out_logs = out_logs.split('\n')
    truncate_out_logs = list_out_logs[-30:]
    tag = '\n'
    last_out_logs = '\n输出日志最后30行:\n' + tag.join(truncate_out_logs)
    return last_out_logs