# -*- coding: utf-8 -*-
# @Time    : 2020/9/29 13:42
# @Author  : wangyinghao
# @FileName: run_ui_test_case.py
# @Software: PyCharm

from selenium import webdriver
from automated_main.view.ui_automation.ui_test_case.ui_automation import base
from automated_main.view.ui_automation.ui_test_case.ui_automation import logs
from automated_main.view.ui_automation.ui_test_case.ui_automation.report import HTMLTestReportCN
import sys
import json
import os,django
import re
import unittest
from ddt import ddt, file_data, unpack
import time
import xmlrunner
from os.path import dirname, abspath
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
BASE_PATH = BASE_DIR.replace("\\", "/")
sys.path.append(BASE_PATH)
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_platform.settings")# project_name 项目名称
django.setup()

# 定义扩展的目录
EXTEND_DIR = BASE_PATH + "/ui_test_case_app/ui_automation/"
print("地址信息" + EXTEND_DIR)

@ddt
class UITestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.basecommon = base.BaseCommon(self.driver)
        self.logs = logs.Log()
        self.basecommon.open_url("https://www.baidu.com/")
        self.driver.maximize_window()

    @unpack
    @file_data("test_data_list.json")
    def test_run_ui_cases(self, elements_operation, page_elements_output, by, page_element):
        # 登录
        self.basecommon.send_keys(by, page_element, page_elements_output)
        # self.basecommon.send_keys("name", "wd", "测试")
        # self.basecommon + "." + elements_operation + (by, page_element, page_elements_output)

    def tearDown(self):
        time.sleep(10)
        self.driver.quit()


def run_cases2():
    now = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
    testunit = unittest.TestSuite()
    testunit.addTest(unittest.TestLoader().loadTestsFromTestCase(UITestCase))
    filename = EXTEND_DIR + 'results.html'
    with open(filename, 'wb') as fp:
        runner = HTMLTestReportCN.HTMLTestRunner(stream=fp,
                                title='自动化测试报告',
                                description=now,
                                verbosity=2)
        runner.run(testunit)

if __name__ == '__main__':
    # suite = unittest.TestLoader.loadTestsFromTestCase(UITestCase)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    run_cases2()
