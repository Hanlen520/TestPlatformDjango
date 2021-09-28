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
import logging
logger = logging.getLogger('django')
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
BASE_PATH = BASE_DIR.replace("\\", "/")
sys.path.append(BASE_PATH)
curPath = os.path.abspath(os.path.dirname(__file__))
logger.info("这是curPath" + curPath)
rootPath = os.path.split(curPath)[0]
logger.info("这是rootPath" + rootPath)
sys.path.append(rootPath)
logger.info("这是rootPath" + rootPath)
sys.path.extend(['/home/AutomatedTestPlatform'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutomatedTestPlatform.settings")  # project_name 项目名称
django.setup()

from automated_main.models.ui_automation.ui_element_operation import UIElementsOperation
from automated_main.models.ui_automation.ui_test_case import UITestCase
from automated_main.models.ui_automation.ui_page_element import UIPageElement
from automated_main.view.ui_automation.ui_test_task.extend.report.HTMLTestReportCN import HTMLTestRunner
from selenium import webdriver
import random
from django.conf import settings
from AutomatedTestPlatform import settings
from automated_main.view.ui_automation.ui_test_case.ui_automation import base
from automated_main.models.ui_automation.ui_test_task import UITestResultAssociated
import time

logger.info("运行测试文件：" + BASE_PATH)

# 定义扩展的目录
EXTEND_DIR = BASE_PATH + "/ui_test_task/extend/"
logger.info("地址信息" + EXTEND_DIR)

# fn = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
# fn = fn + '-%d' % random.randint(0, 100)
# path = os.path.join(settings.WEB_ROOT, fn)
# filename = path + '.py'
# print(path)


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
            ui_task_id = (case['ui_task_id'])
            ui_result_id = (case['ui_result_id'])
            ui_test_case_name = (case['ui_test_case_name'])
            case_steps = (case['case_steps'])
            filename = (case['ui_test_script'])

            elements_operation = UIElementsOperation.objects.get(id=elements_operation_id)

            page_element = UIPageElement.objects.get(id=ui_elements_id)
            element_more = None
            if page_element.ui_page_element_more == "" or page_element.ui_page_element_more is None:
                element_more = None
            else:
                element_more = int(page_element.ui_page_element_more)

            try:

                # 打开浏览器
                if elements_operation.elements_operation_name == "open_url":
                    self.bases.open_url(page_element.ui_page_element)
                    self.driver.maximize_window()
                    time.sleep(int(waiting_time))
                    logger.info("打开url" + str(page_element.ui_page_element))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.open_url" + "(" + '"' + page_element.ui_page_element + '") \n'))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))

                # 输入
                if elements_operation.elements_operation_name == "send_keys":
                    self.bases.send_keys(page_element.ui_element_positioning.locating_method,
                                         page_element.ui_page_element.replace('"', "'"), element_input, element_more)
                    time.sleep(int(waiting_time))
                    logger.info("元素输入操作：" + str(page_element.ui_page_element_name))

                    with open(filename, "a") as f_write:
                        f_write.write(
                            str("self.bases.send_keys" + "(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + "," + '"' + element_input + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))

                # 点击
                if elements_operation.elements_operation_name == "click":
                    self.bases.click(page_element.ui_element_positioning.locating_method, page_element.ui_page_element.replace('"', "'"), element_more)
                    time.sleep(int(waiting_time))
                    logger.info("元素点击操作：" + str(page_element.ui_page_element_name))

                    with open(filename, "a") as f_write:
                        f_write.write(
                            str("self.bases.click" + "(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))

                # 双击
                if elements_operation.elements_operation_name == "double_click":
                    self.bases.double_click(page_element.ui_element_positioning.locating_method,
                                            page_element.ui_page_element, element_more)
                    time.sleep(int(waiting_time))
                    logger.info("元素双击操作：" + str(page_element.ui_page_element_name))

                    with open(filename, "a") as f_write:
                        f_write.write(
                            str("self.bases.double_click" + "(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                # 浏览器后退按钮
                if elements_operation.elements_operation_name == "back":
                    self.bases.back()
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.back() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("浏览器后退按钮：" + str(page_element.ui_page_element_name))

                # 浏览器前进按钮
                if elements_operation.elements_operation_name == "forward":
                    self.bases.forward()
                    time.sleep(int(waiting_time))
                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.forward() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("浏览器前进按钮：" + str(page_element.ui_page_element_name))

                # 关闭浏览器
                if elements_operation.elements_operation_name == "close":
                    self.bases.close()
                    time.sleep(int(waiting_time))
                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.close() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("关闭浏览器：" + str(page_element.ui_page_element_name))

                # 刷新
                if elements_operation.elements_operation_name == "fresh":
                    self.bases.fresh()
                    time.sleep(int(waiting_time))
                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.fresh() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("刷新当前页面：" + str(page_element.ui_page_element_name))

                # send_key输入,可上传图片
                if elements_operation.elements_operation_name == "send_key":
                    self.bases.send_key(page_element.ui_element_positioning.locating_method,
                                        page_element.ui_page_element.replace('"', "'"), element_input, element_more)
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.send_key(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + "," + '"' + element_input + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("send_key输入,可上传图片：" + str(page_element.ui_page_element_name))

                # 重写switch_frame方法
                if elements_operation.elements_operation_name == "frame":
                    self.bases.switch_frame(page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))
                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.switch_frame(" + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))

                    logger.info("switch_frame方法：" + str(page_element.ui_page_element_name))

                # 切换alert弹窗
                if elements_operation.elements_operation_name == "switch_to_alert":
                    self.bases.switch_to_alert(page_element.ui_element_positioning.locating_method,
                                               page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.switch_to_alert(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("切换alert弹窗：" + str(page_element.ui_page_element_name))

                # 鼠标长按左键
                if elements_operation.elements_operation_name == "click_and_hold":
                    self.bases.click_and_hold(page_element.ui_element_positioning.locating_method,
                                              page_element.ui_page_element.replace('"', "'"), element_more)
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.click_and_hold(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))

                    logger.info("鼠标长按左键：" + str(page_element.ui_page_element_name))

                # selenium 获取网页Title
                if elements_operation.elements_operation_name == "get_page_title":
                    self.bases.get_page_title()
                    time.sleep(int(waiting_time))
                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.get_page_title() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("获取网页Title：" + str(page_element.ui_page_element_name))

                # 获取当前URL
                if elements_operation.elements_operation_name == "get_current_url":
                    self.bases.get_current_url()
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.get_current_url() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("获取当前URL：" + str(page_element.ui_page_element_name))

                # 设置窗口最大化
                if elements_operation.elements_operation_name == "set_max_window":
                    self.bases.set_max_window()
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.set_max_window() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("设置窗口最大化：" + str(page_element.ui_page_element_name))

                # 拖拽元素
                if elements_operation.elements_operation_name == "drag_and_drop":
                    self.bases.drag_and_drop(page_element.ui_element_positioning.locating_method,
                                             page_element.ui_page_element.replace('"', "'"), element_more)
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.drag_and_drop(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("拖拽元素：" + str(page_element.ui_page_element_name))

                # 滑动滚动条
                if elements_operation.elements_operation_name == "script":
                    self.bases.script(page_element.ui_element_positioning.locating_method, page_element.ui_page_element.replace('"', "'"),
                                      x_coordinates, y_coordinates, element_more)
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.script(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + "," + '"' + x_coordinates + '"' + "," + '"' + y_coordinates + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("滑动滚动条：" + str(page_element.ui_page_element_name))

                # 元素高亮显示
                if elements_operation.elements_operation_name == "high_light":
                    self.bases.high_light(page_element.ui_element_positioning.locating_method,
                                          page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.high_light(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("元素高亮显示：" + str(page_element.ui_page_element_name))

                # 鼠标悬浮
                if elements_operation.elements_operation_name == "mouse_suspension":
                    self.bases.mouse_suspension(page_element.ui_element_positioning.locating_method,
                                                page_element.ui_page_element.replace('"', "'"), element_more)
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.mouse_suspension(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("鼠标悬浮：" + str(page_element.ui_page_element_name))

                # 鼠标单击（坐标）
                if elements_operation.elements_operation_name == "mouse_click":
                    self.bases.mouse_click(page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.mouse_click(" + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("鼠标单击（坐标）：" + str(page_element.ui_page_element_name))

                # 切换窗口
                if elements_operation.elements_operation_name == "change_window_handle":
                    self.bases.change_window_handle()
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.change_window_handle() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("切换窗口：" + str(page_element.ui_page_element_name))

                # 复制粘贴
                if elements_operation.elements_operation_name == "copy":
                    self.bases.copy()
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.copy() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("复制粘贴：" + str(page_element.ui_page_element_name))

                # js查找元素方式，或jQuery
                if elements_operation.elements_operation_name == "ExcuteJs":
                    self.bases.ExcuteJs(page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.ExcuteJs(" + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("js查找元素方式：" + str(page_element.ui_page_element_name))

                # 全选
                if elements_operation.elements_operation_name == "input":
                    self.bases.input(page_element.ui_element_positioning.locating_method, page_element.ui_page_element.replace('"', "'"),
                                     element_input)
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.input(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element .replace('"', "'")+ '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("全选：" + str(page_element.ui_page_element_name))

                # 关闭新打开页面
                if elements_operation.elements_operation_name == "close_new_window":
                    self.bases.close_new_window()
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.close_new_window() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("关闭新打开页面：" + str(page_element.ui_page_element_name))

                # 利用键盘清空输入框内容
                if elements_operation.elements_operation_name == "keyboard_clear_contents":
                    self.bases.keyboard_clear_contents(page_element.ui_element_positioning.locating_method,
                                                       page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.keyboard_clear_contents(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("利用键盘清空输入框内容：" + str(page_element.ui_page_element_name))

                # 回车
                if elements_operation.elements_operation_name == "enter":
                    self.bases.enter(page_element.ui_element_positioning.locating_method, page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.enter(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("回车：" + str(page_element.ui_page_element_name))

                # 鼠标事件(鼠标悬浮在mouse元素上，移动到x，y坐标并点击)
                if elements_operation.elements_operation_name == "mouse_suspension_click":
                    self.bases.mouse_suspension_click(page_element.ui_element_positioning.locating_method,
                                                      page_element.ui_page_element.replace('"', "'"), x_coordinates, y_coordinates)
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.mouse_suspension_click(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + "," + '"' + x_coordinates + '"' + "," + '"' + y_coordinates + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("鼠标事件(鼠标悬浮在mouse元素上，移动到x，y坐标并点击)：" + str(page_element.ui_page_element_name))

                # 获取元素的坐标
                if elements_operation.elements_operation_name == "get_element_coordinate":
                    self.bases.get_element_coordinate(page_element.ui_element_positioning.locating_method,
                                                      page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.get_element_coordinate(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("获取元素的坐标：" + str(page_element.ui_page_element_name))

                # 获取元素的属性值
                if elements_operation.elements_operation_name == "get_element_value":
                    self.bases.get_element_value(page_element.ui_element_positioning.locating_method,
                                                 page_element.ui_page_element.replace('"', "'"), element_input)
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.get_element_value(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + "," + '"' + element_input + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("获取元素的属性值：" + str(page_element.ui_page_element_name))

                # 获取元素的大小
                if elements_operation.elements_operation_name == "get_element_size":
                    self.bases.get_element_value(page_element.ui_element_positioning.locating_method,
                                                 page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))
                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.get_element_value(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("获取元素的大小：" + str(page_element.ui_page_element_name))

                # 检查元素是否可见
                if elements_operation.elements_operation_name == "get_element_is_displayed":
                    self.bases.get_element_is_displayed(page_element.ui_element_positioning.locating_method,
                                                        page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.get_element_is_displayed(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("检查元素是否可见：" + str(page_element.ui_page_element_name))

                # 检查元素是否被选中(一般用于单选或复选框)
                if elements_operation.elements_operation_name == "get_element_is_selected":
                    self.bases.get_element_is_selected(page_element.ui_element_positioning.locating_method,
                                                       page_element.ui_page_element.replace('"', "'"))
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.get_element_is_selected(" + '"' + page_element.ui_element_positioning.locating_method + '"' + "," + '"' + page_element.ui_page_element.replace('"', "'") + '"' + ") \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("查元素是否被选中：" + str(page_element.ui_page_element_name))

                # 获取浏览器名字
                if elements_operation.elements_operation_name == "get_browser_name":
                    self.bases.get_browser_name()
                    time.sleep(int(waiting_time))

                    with open(filename, "a") as f_write:
                        f_write.write(str("self.bases.get_browser_name() \n"))
                        f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))
                    logger.info("获取浏览器名字：" + str(page_element.ui_page_element_name))

                ui_successful = 1
                ui_error = 0
                abnormal = ""

                UITestResultAssociated.objects.create(ui_task_id=ui_task_id, ui_result_id=ui_result_id,
                                                      ui_error=ui_error, ui_successful=ui_successful, abnormal=abnormal,
                                                      ui_test_case_name=ui_test_case_name)

            except Exception as e:
                logger.info("这是错误的步骤页面信息: " + str(page_element.ui_page_element_name))
                logger.info("这是异常信息: " + str(e))

                ui_error = 1
                ui_successful = 0
                abnormal = "这是错误的页面名称: " + str(page_element.ui_page.ui_page_name) + ",这是错误的页面元素名称: " + str(
                    page_element.ui_page_element_name) + "，这是错误的步骤: " + str(case_steps) + ",这是异常信息: " + str(e)

                with open(filename, "a") as f_write:
                    f_write.write(str("这是错误的页面名称: " + str(page_element.ui_page.ui_page_name) + ",这是错误的页面元素名称: " + str(page_element.ui_page_element_name) + "，这是错误的步骤: " + str(case_steps) + ",这是异常信息: " + str(e))  + "\n")

                    f_write.write(str(elements_operation.elements_operation_name + "(" + "'" + page_element.ui_element_positioning.locating_method + "', " + '"' + page_element.ui_page_element + '") \n'))
                    f_write.write(str("time.sleep" + "(" + waiting_time + ") \n"))

                UITestResultAssociated.objects.create(ui_task_id=ui_task_id, ui_result_id=ui_result_id,
                                                      ui_error=ui_error, ui_successful=ui_successful, abnormal=abnormal,
                                                      ui_test_case_name=ui_test_case_name)
                break

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()
        pass


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
    # run_cases2()
    unittest.main(verbosity=2)
