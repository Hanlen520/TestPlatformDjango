# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 17:59
# @Author  : wangyinghao
# @FileName: ui_element_positioning.py
# @Software: PyCharm
from django.db import models


class UIPositioning(models.Model):
    """
    UI定位管理表
    """
    positioning_name = models.CharField("定位方法名称", max_length=50, null=False)
    locating_method = models.CharField("定位方法", max_length=200, null=False)
    describe = models.TextField("描述", default="", null=True)
    status = models.BooleanField("状态", default=True)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.positioning_name
