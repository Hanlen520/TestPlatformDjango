# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 14:37
# @Author  : wangyinghao
# @FileName: api_test_task.py
# @Software: PyCharm
from django.db import models
from automated_main.models.api_automation.api_project import APIProject


class APITestTask(models.Model):
    """
    API任务表
    """
    api_test_task_name = models.CharField("API测试任务名称", max_length=100, blank=False, default="")
    describe = models.TextField("描述", default="", null=True)
    status = models.IntegerField("状态：", default=0)  # 未执行、执行中、执行完成、排队中
    cases = models.TextField("关联API用例", default="")
    api_project = models.ForeignKey(APIProject, on_delete=models.CASCADE)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.api_test_task_name


class APITestResult(models.Model):
    """
    API测试结果表
    """
    api_test_result_name = models.CharField("api测试报告名称", max_length=200, blank=False, default="")
    api_task = models.ForeignKey(APITestTask, on_delete=models.CASCADE)
    api_error_total_number = models.CharField("失败总数", max_length=100, null=True, blank=True)
    api_successful_total_number = models.CharField("成功总数", max_length=100, null=True, blank=True)
    api_total_number = models.CharField("API总数", max_length=100, null=True, blank=True)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.api_test_result_name


class APITestResultAssociated(models.Model):
    """
    API测试结果关联表
    """
    api_test_case_name = models.CharField("api测试用例名称", max_length=100, blank=False, default="")
    api_task = models.ForeignKey(APITestTask, on_delete=models.CASCADE)
    api_result = models.ForeignKey(APITestResult, on_delete=models.CASCADE)
    api_error = models.CharField("失败", max_length=100, null=True, blank=True)
    api_successful = models.CharField("成功", max_length=100, null=True, blank=True)
    abnormal = models.TextField("异常", max_length=5000, null=True, blank=True)
    json_extract_variable_conversion = models.TextField("json提取变量转换", max_length=5000, null=True, blank=True)
    api_assertion_results = models.TextField("断言结果", max_length=5000, null=True, blank=True)
    api_variable_results = models.TextField("参数提取", max_length=5000, null=True, blank=True)
    api_request_results = models.JSONField("API请求结果", null=True, default=None)
    api_business_test_name = models.TextField("API业务测试名称", max_length=5000, null=True, blank=True)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.api_test_case_name


