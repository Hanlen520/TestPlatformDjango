# -*- coding: utf-8 -*-
# @Time    : 2021/3/2 18:46
# @Author  : wangyinghao
# @FileName: api_project.py
# @Software: PyCharm
from django import forms


class ApiProjectForm(forms.Form):
    api_project_name = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "API项目名称不能为空"})

    describe = forms.CharField(max_length=2000,
                               min_length=2,
                               required=False,
                               error_messages={'required': "描述超过2000字符"})

