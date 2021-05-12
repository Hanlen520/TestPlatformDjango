# -*- coding: utf-8 -*-
# @Time    : 2021/4/15 18:14
# @Author  : wangyinghao
# @FileName: api_business_test.py
# @Software: PyCharm
from django import forms


class ApiBusinessTestForm(forms.Form):
    api_business_test_name = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "Api业务测试名称不能为空"})

    api_project_id = forms.CharField(required=False)
