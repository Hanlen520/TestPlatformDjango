# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 11:30
# @Author  : wangyinghao
# @FileName: ui_element_operation.py
# @Software: PyCharm
from django.db import models

# Create your models here.


class UIElementsOperation(models.Model):
    """
    UI元素操作表
    """
    elements_operation_name = models.CharField("元素操作名称", max_length=500, null=False)
    elements_operation_title = models.CharField("元素操作标题", max_length=500, null=False)
    elements_operation_describe = models.TextField("描述", default="", null=True)
    status = models.BooleanField("状态", default=True)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.elements_operation_name
