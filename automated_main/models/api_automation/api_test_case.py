# -*- coding: utf-8 -*-
# @Time    : 2021/3/29 17:30
# @Author  : wangyinghao
# @FileName: api_test_case.py
# @Software: PyCharm
from django.db import models
from automated_main.models.api_automation.api_module import APIModule
from automated_main.models.api_automation.api_environment import APIEnvironment


class ApiTestCase(models.Model):
    """
    Api测试用例表
    """
    api_test_case_name = models.CharField("API测试用例名称", max_length=100, null=False)
    api_module = models.ForeignKey(APIModule, on_delete=models.CASCADE)
    api_environment = models.ForeignKey(APIEnvironment, on_delete=models.CASCADE)
    api_method = models.IntegerField("请求方法", null=False)  # 1:get 2.post 3:put 4:delete
    api_url = models.TextField("API请求地址", null=False)
    api_parameter_types = models.IntegerField("参数类型", null=False)  # 1：form-data 2: json 3:x-www-form-urlencoded
    api_headers = models.TextField("请求头", null=False)
    api_parameter_body = models.TextField("参数内容", null=False)
    api_assert_type = models.IntegerField("断言类型", null=False)  # 1：包含contains 2: 匹配mathches
    api_assert_text = models.TextField("断言结果", null=False)
    api_variable_results = models.CharField("变量提取结果", max_length=200, null=True)
    api_value_variable = models.CharField("提取变量", max_length=200, null=True)
    api_key_variable = models.CharField("关键字变量名称", max_length=200, null=True)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.api_test_case_name

