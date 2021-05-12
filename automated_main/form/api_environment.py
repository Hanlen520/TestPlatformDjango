# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 16:57
# @Author  : wangyinghao
# @FileName: api_environment.py
# @Software: PyCharm
from django import forms


class ApiEnvironmentForm(forms.Form):
    api_environment_name = forms.CharField(max_length=200,
                               min_length=2,
                               required=True,
                               error_messages={'required': "API环境名称不能为空"})

    api_title = forms.CharField(max_length=200,
                               min_length=2,
                               required=True,
                               error_messages={'required': "API环境标题不能为空"})

    api_environment_describe = forms.CharField(max_length=200,
                               min_length=2,
                               required=False,
                               error_messages={'required': "描述超过2000字符"})
