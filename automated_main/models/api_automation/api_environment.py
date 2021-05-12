# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 15:00
# @Author  : wangyinghao
# @FileName: api_environment.py
# @Software: PyCharm
from django.db import models


class APIEnvironment(models.Model):
    """
    API环境设置
    """
    api_environment_name = models.CharField("API环境名称", max_length=200, null=False)
    api_title = models.CharField("API环境标题名称", max_length=200, null=False)
    api_environment_describe = models.TextField("API环境描述", default="", null=True)
    status = models.BooleanField("状态", default=1)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    updata_time = models.DateTimeField("更新时间", auto_now_add=True)

    def __str__(self):
        return self.api_environment_name
