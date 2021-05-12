# -*- coding: utf-8 -*-
# @Time    : 2020/7/4 16:27
# @Author  : wangyinghao
# @FileName: run_task.py
# @Software: PyCharm
import sys
import json
import os, django
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
print("这是curPath",curPath)
rootPath = os.path.split(curPath)[0]
print("这是rootPath",rootPath)
sys.path.append(rootPath)
print("这是rootPath",rootPath)
sys.path.extend(['/home/AutomatedTestPlatform'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutomatedTestPlatform.settings")# project_name 项目名称
django.setup()

from automated_main.models.ui_automation.ui_element_operation import UIElementsOperation
from automated_main.models.ui_automation.ui_test_case import UITestCase
from automated_main.models.ui_automation.ui_page_element import UIPageElement
from automated_main.view.ui_automation.ui_test_task.extend.report.HTMLTestReportCN import HTMLTestRunner
from selenium import webdriver
from automated_main.view.ui_automation.ui_test_case.ui_automation import base
import time

print("运行测试文件：", BASE_PATH)

# 定义扩展的目录
EXTEND_DIR = BASE_PATH + "/ui_test_task/extend/"
print("地址信息" + EXTEND_DIR)

@ddt
class InterfaceTest(unittest.TestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.bases = base.BaseCommon(self.driver)

    @unpack
    @file_data("test_data_list.json")
    def test_run_cases(self, case_id):

        for case in case_id:
            element_input = (case['element_input'])
            x_coordinates = (case['x_coordinates'])
            y_coordinates = (case['y_coordinates'])
            elements_operation_id = (case['element_operation'])
            ui_elements_id = (case['ui_elements_id'])
            waiting_time = (case['waiting_time'])
            elements_operation = UIElementsOperation.objects.get(id=elements_operation_id)
            print("这是data中得数据：", element_input, elements_operation_id, ui_elements_id, waiting_time)
            page_element = UIPageElement.objects.get(id=ui_elements_id)

            # 打开浏览器
            if elements_operation.elements_operation_name == "open_url":
                self.bases.open_url(page_element.ui_page_element)
                self.driver.maximize_window()
                time.sleep(int(waiting_time))

            # 输入
            if elements_operation.elements_operation_name == "send_keys":
                self.bases.send_keys(page_element.ui_element_positioning.locating_method, page_element.ui_page_element, element_input)
                time.sleep(int(waiting_time))

            # 点击
            if elements_operation.elements_operation_name == "click":
                self.bases.click(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 双击
            if elements_operation.elements_operation_name == "double_click":
                self.bases.double_click(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 浏览器后退按钮
            if elements_operation.elements_operation_name == "back":
                self.bases.back()
                time.sleep(int(waiting_time))

            # 浏览器前进按钮
            if elements_operation.elements_operation_name == "forward":
                self.bases.forward()
                time.sleep(int(waiting_time))

            # 关闭浏览器
            if elements_operation.elements_operation_name == "close":
                self.bases.close()
                time.sleep(int(waiting_time))

            # 刷新
            if elements_operation.elements_operation_name == "fresh":
                self.bases.fresh()
                time.sleep(int(waiting_time))

            # send_key输入,可上传图片
            if elements_operation.elements_operation_name == "send_key":
                self.bases.send_key(page_element.ui_element_positioning.locating_method, page_element.ui_page_element, element_input)
                time.sleep(int(waiting_time))

            # 重写switch_frame方法
            if elements_operation.elements_operation_name == "frame":
                self.bases.switch_frame(page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 切换alert弹窗
            if elements_operation.elements_operation_name == "switch_to_alert":
                self.bases.switch_to_alert(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 鼠标长按左键
            if elements_operation.elements_operation_name == "click_and_hold":
                self.bases.click_and_hold(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # selenium 获取网页Title
            if elements_operation.elements_operation_name == "get_page_title":
                self.bases.get_page_title()
                time.sleep(int(waiting_time))

            # 获取当前URL
            if elements_operation.elements_operation_name == "get_current_url":
                self.bases.get_current_url()
                time.sleep(int(waiting_time))

            # 设置窗口最大化
            if elements_operation.elements_operation_name == "set_max_window":
                self.bases.set_max_window()
                time.sleep(int(waiting_time))

            # 拖拽元素
            if elements_operation.elements_operation_name == "drag_and_drop":
                self.bases.drag_and_drop(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 滑动滚动条
            if elements_operation.elements_operation_name == "script":
                self.bases.script(page_element.ui_element_positioning.locating_method, page_element.ui_page_element, x_coordinates, y_coordinates)
                time.sleep(int(waiting_time))

            # 元素高亮显示
            if elements_operation.elements_operation_name == "high_light":
                self.bases.high_light(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 鼠标悬浮
            if elements_operation.elements_operation_name == "mouse_suspension":
                self.bases.mouse_suspension(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 鼠标单击（坐标）
            if elements_operation.elements_operation_name == "mouse_click":
                self.bases.mouse_click(page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 切换窗口
            if elements_operation.elements_operation_name == "change_window_handle":
                self.bases.change_window_handle()
                time.sleep(int(waiting_time))

            # 复制粘贴
            if elements_operation.elements_operation_name == "copy":
                self.bases.copy()
                time.sleep(int(waiting_time))

            # js查找元素方式，或jQuery
            if elements_operation.elements_operation_name == "ExcuteJs":
                self.bases.ExcuteJs(page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 全选
            if elements_operation.elements_operation_name == "input":
                self.bases.input(page_element.ui_element_positioning.locating_method, page_element.ui_page_element, element_input)
                time.sleep(int(waiting_time))

            # 关闭新打开页面
            if elements_operation.elements_operation_name == "close_new_window":
                self.bases.close_new_window()
                time.sleep(int(waiting_time))

            # 利用键盘清空输入框内容
            if elements_operation.elements_operation_name == "keyboard_clear_contents":
                self.bases.keyboard_clear_contents(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 回车
            if elements_operation.elements_operation_name == "enter":
                self.bases.enter(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 鼠标事件(鼠标悬浮在mouse元素上，移动到x，y坐标并点击)
            if elements_operation.elements_operation_name == "mouse_suspension_click":
                self.bases.mouse_suspension_click(page_element.ui_element_positioning.locating_method, page_element.ui_page_element, x_coordinates, y_coordinates)
                time.sleep(int(waiting_time))

            # 获取元素的坐标
            if elements_operation.elements_operation_name == "get_element_coordinate":
                self.bases.get_element_coordinate(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 获取元素的属性值
            if elements_operation.elements_operation_name == "get_element_value":
                self.bases.get_element_value(page_element.ui_element_positioning.locating_method, page_element.ui_page_element, element_input)
                time.sleep(int(waiting_time))

            # 获取元素的大小
            if elements_operation.elements_operation_name == "get_element_size":
                self.bases.get_element_value(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 检查元素是否可见
            if elements_operation.elements_operation_name == "get_element_is_displayed":
                self.bases.get_element_is_displayed(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 检查元素是否被选中(一般用于单选或复选框)
            if elements_operation.elements_operation_name == "get_element_is_selected":
                self.bases.get_element_is_selected(page_element.ui_element_positioning.locating_method, page_element.ui_page_element)
                time.sleep(int(waiting_time))

            # 获取浏览器名字
            if elements_operation.elements_operation_name == "get_browser_name":
                self.bases.get_browser_name()
                time.sleep(int(waiting_time))

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()



def run_cases():
    with open(EXTEND_DIR + 'results2.xml', 'w') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False
        )


def run_cases2():
    now = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
    testunit = unittest.TestSuite()
    testunit.addTest(unittest.TestLoader().loadTestsFromTestCase(InterfaceTest))
    filename = EXTEND_DIR + 'results.html'
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp,
                                title='自动化测试报告',
                                description=now,
                                verbosity=2)
        runner.run(testunit)


if __name__ == '__main__':
    run_cases2()
    #unittest.main()






