# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 19:04
# @Author  : wangyinghao
# @FileName: ui_test_case.py
# @Software: PyCharm
from django import forms


class UiTestCaseForm(forms.Form):
    ui_test_case_name = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "测试用例名称不能为空"})

    ui_project_id = forms.CharField(required=False)
