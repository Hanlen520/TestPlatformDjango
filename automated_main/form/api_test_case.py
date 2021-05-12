# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 11:24
# @Author  : wangyinghao
# @FileName: api_test_case.py
# @Software: PyCharm
from django import forms


class ApiTestCaseForm(forms.Form):
    api_test_case_name = forms.CharField(max_length=50,
                                         min_length=2,
                                         required=True,
                                         error_messages={'required': "API测试用例名称不能为空",
                                                         'max_length': "API测试用例名称不能超过50个字符",
                                                         'min_length': "API测试用例名称不能少于2个字符",
                                                         }
                                         )

    api_module_id = forms.CharField(required=False)

    api_environment_id = forms.CharField(required=False)

    api_method = forms.CharField(required=False)

    api_url = forms.CharField(required=False)

    api_parameter_types = forms.CharField(required=False)

    api_headers = forms.CharField(required=False)

    api_parameter_body = forms.CharField(required=False)

    api_assert_type = forms.CharField(required=False)

    api_assert_text = forms.CharField(required=False)

    api_variable_results = forms.CharField(required=False)

    api_value_variable = forms.CharField(required=False)

    api_key_variable = forms.CharField(required=False)


