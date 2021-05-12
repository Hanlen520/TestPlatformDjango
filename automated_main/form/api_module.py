# -*- coding: utf-8 -*-
# @Time    : 2021/3/3 11:03
# @Author  : wangyinghao
# @FileName: api_module.py
# @Software: PyCharm
from django import forms


class ApiModuleForm(forms.Form):
    api_module_name = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "API模块名称不能为空"})

    api_module_describe = forms.CharField(max_length=2000,
                               min_length=2,
                               required=False,
                               error_messages={'required': "描述超过2000字符"})

    api_project_id = forms.CharField(required=False)
