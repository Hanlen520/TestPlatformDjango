# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 18:30
# @Author  : wangyinghao
# @FileName: api_test_task.py
# @Software: PyCharm
from django import forms


class ApiTestTaskForm(forms.Form):
    api_test_task_name = forms.CharField(max_length=100,
                                         min_length=2,
                                         required=True,
                                         error_messages={'required': "API测试任务名称不能为空"})

    describe = forms.CharField(required=False)

    cases = forms.CharField(required=False)
    api_project_id = forms.CharField(required=False)
