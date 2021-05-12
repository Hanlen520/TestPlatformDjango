# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 11:02
# @Author  : wangyinghao
# @FileName: setting.py
# @Software: PyCharm
import os
from AutomatedTestPlatform.settings import BASE_DIR

EXTEND_DIR = os.path.join(BASE_DIR, "automated_main/view/api_automation/api_test_task", "extend")
# EXTEND_DIR = os.path.join(BASE_DIR, "automated_main\\view\\api_automation\\api_test_task", "extend")

TASK_RESULTS = os.path.join(EXTEND_DIR, "results.html")

print(TASK_RESULTS)