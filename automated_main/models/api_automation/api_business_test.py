# -*- coding: utf-8 -*-
# @Time    : 2021/4/14 17:20
# @Author  : wangyinghao
# @FileName: api_business_test.py
# @Software: PyCharm
from django.db import models
from automated_main.models.api_automation.api_project import APIProject
from automated_main.models.api_automation.api_module import APIModule
from automated_main.models.api_automation.api_test_case import ApiTestCase


class ApiBusinessTest(models.Model):
    """
    api业务测试表
    """

    api_business_test_name = models.CharField("API业务测试名称", max_length=100, null=False)
    api_project = models.ForeignKey(APIProject, on_delete=models.CASCADE)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.api_business_test_name


class ApiBusinessTestAssociated(models.Model):
    """
    API业务测试关联表
    """
    bid = models.ForeignKey(ApiBusinessTest, on_delete=models.CASCADE)
    api_module = models.ForeignKey(APIModule, on_delete=models.CASCADE)
    api_test_case = models.ForeignKey(ApiTestCase, on_delete=models.CASCADE)
    case_steps = models.CharField("操作步骤", max_length=100, null=False)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return str(self.bid)
