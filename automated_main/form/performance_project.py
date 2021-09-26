# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/27 14:49
@Auth ： WangYingHao
@File ：performance_project.py
@IDE ：PyCharm

"""
from django import forms


class PerformanceProjectForm(forms.Form):
    performance_project_name = forms.CharField(max_length=50,
                                               min_length=2,
                                               required=True,
                                               error_messages={'required': "性能测试项目名称不能为空"})

    describe = forms.CharField(max_length=2000,
                               min_length=2,
                               required=False,
                               error_messages={'required': "描述超过2000字符"})
