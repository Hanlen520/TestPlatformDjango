# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 10:31
# @Author  : wangyinghao
# @FileName: ui_test_task.py
# @Software: PyCharm
from django import forms


class UiTestTaskForm(forms.Form):
    ui_test_task_name = forms.CharField(max_length=100,
                                        min_length=2,
                                        required=True,
                                        error_messages={'required': "UI测试任务名称不能为空"})

    describe = forms.CharField(required=False)

    cases = forms.CharField(required=False)
    ui_project_id = forms.CharField(required=False)


