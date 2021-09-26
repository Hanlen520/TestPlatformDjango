# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 10:09
# @Author  : wangyinghao
# @FileName: ui_test_task.py
# @Software: PyCharm
from django.db import models
from automated_main.models.ui_automation.ui_project import UIProject


class UITestTask(models.Model):
    """
    任务表
    """
    ui_test_task_name = models.CharField("UI测试任务名称", max_length=100, blank=False, default="")
    describe = models.TextField("描述", default="", null=True)
    status = models.IntegerField("状态：", default=0)  # 未执行、执行中、执行完成、排队中
    cases = models.TextField("关联UI用例", default="")
    ui_project = models.ForeignKey(UIProject, on_delete=models.CASCADE)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.ui_test_task_name


class UITestResult(models.Model):
    """
    测试结果表
    """
    ui_test_result_name = models.CharField("UI测试报告名称", max_length=100, blank=False, default="")
    ui_task = models.ForeignKey(UITestTask, on_delete=models.CASCADE)
    ui_error_total_number = models.CharField("失败总数", max_length=100, null=True, blank=True)
    ui_total_number = models.CharField("UI测试用例总数", max_length=100, null=True, blank=True)
    ui_successful_total_number = models.CharField("成功总数", max_length=100, null=True, blank=True)
    ui_test_script = models.CharField("UI测试脚本", max_length=1000, blank=False, default="", null=True)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.ui_test_result_name


class UITestResultAssociated(models.Model):
    """
    UI测试结果关联表
    """
    ui_test_case_name = models.CharField("ui测试用例名称", max_length=100, blank=False, default="")
    ui_task = models.ForeignKey(UITestTask, on_delete=models.CASCADE)
    ui_result = models.ForeignKey(UITestResult, on_delete=models.CASCADE)
    ui_error = models.CharField("失败", max_length=100, null=True, blank=True)
    ui_successful = models.CharField("成功", max_length=100, null=True, blank=True)
    abnormal = models.TextField("异常", max_length=5000, null=True, blank=True)
    ui_assertion_results = models.TextField("断言结果", max_length=5000, null=True, blank=True)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.ui_test_case_name

