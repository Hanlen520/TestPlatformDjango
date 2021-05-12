# -*- coding: utf-8 -*-
# @Time    : 2020/12/9 14:42
# @Author  : wangyinghao
# @FileName: ui_project.py
# @Software: PyCharm
from django import forms


class UiProjectForm(forms.Form):
    ui_project_name = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "项目名称不能为空"})

    describe = forms.CharField(max_length=2000,
                               min_length=2,
                               required=False,
                               error_messages={'required': "描述超过2000字符"})

