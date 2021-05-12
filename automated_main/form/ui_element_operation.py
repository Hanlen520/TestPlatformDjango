# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 11:33
# @Author  : wangyinghao
# @FileName: ui_element_operation.py
# @Software: PyCharm
from django import forms


class UIElementsOperationForm(forms.Form):

    elements_operation_name = forms.CharField(max_length=500,
                                              min_length=2,
                                              required=True,
                                              error_messages={'required': "元素操作名称不能为空"})

    elements_operation_title = forms.CharField(max_length=500,
                                               min_length=2,
                                               required=False,
                                               error_messages={'required': "元素操作标题不能为空"})

    elements_operation_describe = forms.CharField(max_length=2000,
                                                  min_length=2,
                                                  required=False,
                                                  error_messages={'required': "描述超过2000字符"})

