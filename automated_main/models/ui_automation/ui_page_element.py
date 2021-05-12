# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 15:22
# @Author  : wangyinghao
# @FileName: ui_page_element.py
# @Software: PyCharm
from django.db import models
from automated_main.models.ui_automation.ui_project import UIProject
from automated_main.models.ui_automation.ui_page import UIPage
from automated_main.models.ui_automation.ui_element_positioning import UIPositioning


class UIPageElement(models.Model):
    """
    UI页面元素
    """
    ui_project = models.ForeignKey(UIProject, on_delete=models.CASCADE)
    ui_page = models.ForeignKey(UIPage, on_delete=models.CASCADE)
    ui_page_element_name = models.CharField("UI页面元素名称", max_length=100, null=False)
    ui_page_element = models.CharField("UI页面元素", max_length=600, null=False)
    ui_element_positioning = models.ForeignKey(UIPositioning, on_delete=models.CASCADE)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    updata_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ui_page_element_name
