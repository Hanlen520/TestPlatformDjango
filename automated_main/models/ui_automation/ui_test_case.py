# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 18:46
# @Author  : wangyinghao
# @FileName: ui_test_case.py
# @Software: PyCharm
from django.db import models
from automated_main.models.ui_automation.ui_project import UIProject
# from ui_page_app.models import UIPage
from automated_main.models.ui_automation.ui_page_element import UIPageElement


# Create your models here.
class UITestCase(models.Model):
    """
    UI测试用例表
    """
    ui_test_case_name = models.CharField("UI测试用例名称", max_length=100, null=False)
    ui_project = models.ForeignKey(UIProject, on_delete=models.CASCADE)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.ui_test_case_name


class UITestCaseAssociated(models.Model):
    """
    UI测试用例关联表
    """
    cid = models.ForeignKey(UITestCase, on_delete=models.CASCADE)
    ui_page_elements = models.ForeignKey(UIPageElement, on_delete=models.CASCADE, null=True)
    element_operation = models.CharField("元素操作", max_length=100, null=False)
    element_input = models.CharField("元素输出", max_length=100, null=True, blank=True)
    x_coordinates = models.CharField("X坐标", max_length=100, null=True, blank=True)
    y_coordinates = models.CharField("Y坐标", max_length=100, null=True, blank=True)
    waiting_time = models.CharField("等待时间", max_length=100, null=True)
    case_steps = models.CharField("操作步骤", max_length=100, null=True)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return str(self.cid_id)
