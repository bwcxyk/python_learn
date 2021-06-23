#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name  :    dd_form.py
   Description:
   Author     :    Deniss.Wang
   date       :    2019/../..
-------------------------------------------------
   Change Activity:
                   2019/../..
-------------------------------------------------
"""
import requests
import json
import os
from conf import config

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
approve_id_file_path = os.path.join(base_dir, 'spid', 'approve_id.txt')

# dd approve configure
dd_id = config.corpid
dd_secret = config.secret
dd_url = config.dd_url
dd_method = config.dd_method
dd_form_code = config.dd_form_code_for_java
dd_headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
time_format = 'yyyy-MM-dd HH:mm:ss'

get_dd_token = requests.get("https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s" % (dd_id, dd_secret),
                            timeout=20)
json_dd_token = json.loads(get_dd_token.text)
DD_ACCESS_TOKEN = json_dd_token["access_token"]

# Parameter
payload = dict(format='json', method=dd_method,
               session=DD_ACCESS_TOKEN, timestamp=time_format, v='2.0', cursor=0,
               process_code=dd_form_code, size=1, start_time='1196678400000')


def init_approve_id_list():
    '''
    # Initialize dd approve id to file
    :return:
    '''

    payload_init = dict(format='json', method=dd_method,
                   session=DD_ACCESS_TOKEN, timestamp=time_format, v='2.0', cursor=0,
                   process_code=dd_form_code, size=10, start_time='1196678400000')

    approve_id_file = open(approve_id_file_path, 'w+')
    approve_id_list = []

    while True:
        req = requests.post(dd_url, data=payload_init, headers=dd_headers, timeout=15).json()
        projectList = req.get('dingtalk_smartwork_bpms_processinstance_list_response', '').get('result', '').get(
            'result', '').get('list', '')
        if len(projectList) == 0:
            break

        next_page = req.get('dingtalk_smartwork_bpms_processinstance_list_response', '').get('result', '').get('result',
                                                                                                              '').get(
            'next_cursor', '')

        for res in req['dingtalk_smartwork_bpms_processinstance_list_response']['result']['result']['list'][
            'process_instance_top_vo']:
            approve_Instance_Result = res['process_instance_result']
            approveStatus = res['status']
            if approve_Instance_Result == "agree" and approveStatus == "COMPLETED":
                approveId = res.get('process_instance_id', '')
                approve_id_file.write(approveId + '\n')
                approve_id_list.append(approveId)
        payload_init['cursor'] = int(next_page)
        approve_id_file.close()


def dd_approve_check():
    '''
    :return:
    '''

    # Request
    proj_name = ''
    form_req = requests.post(dd_url, data=payload, headers=dd_headers, timeout=15).json()
    print(form_req)
    for form_res in form_req['dingtalk_smartwork_bpms_processinstance_list_response']['result']['result']['list'][
        'process_instance_top_vo']:
        approve_Instance_Result = form_res['process_instance_result']
        approve_Status = form_res['status']

        if approve_Instance_Result == "agree" and approve_Status == "COMPLETED":
            approve_id = form_res['process_instance_id']
            approve_id_file = open(approve_id_file_path, 'r+')
            approve_id_list = [approve_id_check.replace('\n', '') for approve_id_check in approve_id_file.readlines()]

            if approve_id in approve_id_list:
                return 'approve_pass', 'pass', proj_name

            else:
                approve_id_file.write(approve_id + '\n')
                approve_id_file.close()

                # Get the dingding user mobile && cname
                approve_userid = form_res['originator_userid']
                user_Info_Url = 'https://oapi.dingtalk.com/user/get?access_token=%s&userid=%s' % (
                DD_ACCESS_TOKEN, approve_userid)
                get_User_Info = requests.get(user_Info_Url, timeout=10).json()
                print('get_user_info', get_User_Info)
                get_User_Mobile = get_User_Info['mobile']

                #form_component_values = form_res.get('form_component_values').get('form_component_value_vo')
                ##project_name = form_component_values[0].get('value')
                #project_summary = form_component_values[1].get('value')
                #project_expire = form_component_values[4].get('value')
                #project_plan = form_component_values[5].get('value')
                #project_remark = form_component_values[6].get('value')
                #form_content = f'''
#项目名称: {project_name}
#项目概述: {project_summary}
#期望启动时间: {project_expire}
#计划进度: {project_plan}
#备注: {project_remark}'''
                items = form_res['form_component_values']['form_component_value_vo']
                for item in items:
                    if item['name'] == '单选框':
                        proj_name = item['value']

                return get_User_Mobile, proj_name, proj_name
        else:
            return 'approve_pass', 'pass', proj_name