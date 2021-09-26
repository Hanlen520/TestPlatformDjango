# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/27 18:02
@Auth ： WangYingHao
@File ：performance_script.py
@IDE ：PyCharm

"""
from django import forms


class PerformanceScriptForm(forms.Form):
    performance_script_name = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "性能脚本名称不能为空"})

    performance_script = forms.CharField(max_length=5000,
                               min_length=2,
                               required=True,
                               error_messages={'required': "性能脚本不能为空"})

    performance_project_id = forms.CharField(required=False)
