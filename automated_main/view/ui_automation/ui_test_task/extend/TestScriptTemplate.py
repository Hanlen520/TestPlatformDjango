# -*- coding: utf-8 -*-
# @Time    : 2019/6/18 10:34
# @Author  : wangyinghao
# @FileName: Test.py
# @Software: PyCharm

from selenium import webdriver
import unittest
import time
from automated_main.view.ui_automation.ui_test_case.ui_automation import base


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.bases = base.BaseCommon(self.driver)
        self.driver.maximize_window()

    def test01(self):
        """
        此处填写Web自动化脚本
        :return:
        """

    def tearDown(self):
        time.sleep(5)
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader.loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
