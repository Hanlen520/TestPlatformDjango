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
    error = models.IntegerField("错误用例")
    failure = models.IntegerField("失败用例")
    skipped = models.IntegerField("跳过用例")
    tests = models.IntegerField("总用例数")
    run_time = models.CharField("运行时长", max_length=200, blank=False, default="")
    result = models.TextField("详细", default="")
    successful = models.IntegerField("成功用例")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.ui_test_result_name

