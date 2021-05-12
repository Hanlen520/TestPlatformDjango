# -*- coding: utf-8 -*-
# @Time    : 2021/3/3 10:57
# @Author  : wangyinghao
# @FileName: api_module.py
# @Software: PyCharm
from django.db import models
from automated_main.models.api_automation.api_project import APIProject


class APIModule(models.Model):
    """
    API模块表
    """
    api_project = models.ForeignKey(APIProject, on_delete=models.CASCADE, null=True)
    api_module_name = models.CharField("API模块名称", max_length=50, null=False)
    api_module_describe = models.TextField("API模块描述", default="", null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    updata_time = models.DateTimeField("更新时间", auto_now_add=True)

    def __str__(self):
        return self.api_module_name
