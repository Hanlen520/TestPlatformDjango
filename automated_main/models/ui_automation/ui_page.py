# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 18:15
# @Author  : wangyinghao
# @FileName: ui_page.py
# @Software: PyCharm
from django.db import models
from automated_main.models.ui_automation.ui_project import UIProject


class UIPage(models.Model):
    """
    UI页面表
    """
    ui_project = models.ForeignKey(UIProject, on_delete=models.CASCADE, null=True)
    ui_page_name = models.CharField("UI页面名称", max_length=50, null=False)
    ui_page_describe = models.TextField("UI页面描述", default="", null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    updata_time = models.DateTimeField("更新时间", auto_now_add=True)

    def __str__(self):
        return self.ui_page_name

