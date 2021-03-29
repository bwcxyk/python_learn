#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name  :    start.py
   Description:
   Author     :    Deniss.Wang
   date       :    2019/11/12
-------------------------------------------------
   Change Activity:
                   2019/../..
-------------------------------------------------
"""


import os
import sys
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)


from lib import message
from lib import dd_form
from lib import oms



if __name__ == '__main__':

    ## Initialize dd approve id to file
    # dd_form.init_approve_id_list()
    # exit(0)

    project_job_name = {
        "adcloud-api": 'auto_deploy1',
        "adcloud-web": 'auto_deploy2'
    }
    #JOB_NAME = 'auto_deploy'	# jenkins job name
    #print(JOB_NAME)

    try:
        ## get approve user_mobile and form_content
        dd_user_mobile, content, proj_name = dd_form.dd_approve_check()
        content = 'project name:' + content
        print('dd_user_mobile:', dd_user_mobile)
        if dd_user_mobile != "approve_pass":
            job_name = project_job_name[proj_name]
            print('Dingtalk 审批通过，%s 正在上线, 请稍后...' % job_name)
            message.send_online_msg('Dingtalk 审批通过，%s 正在上线, 请稍后...' % job_name)
            dh_job_build_result, dh_job_executable_number = oms.code_update(job_name)
            print(2)
            out_logs = oms.get_job_build_log(job_name, dh_job_executable_number)
            print(3)
            msg_content = content + out_logs
            print(msg_content)
            message.send_notification_by_ddRobot(dd_user_mobile, msg_content)
            print(4)
        else:
            print("没有审批")
            import time
            time.sleep(1)

    except Exception as e:
        print(e)
        exit(0)


