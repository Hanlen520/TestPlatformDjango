# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 16:10
# @Author  : wangyinghao
# @FileName: ui_page_element.py
# @Software: PyCharm
from django import forms


class UiPageElementForm(forms.Form):
    # ui_page_element_name = forms.CharField(max_length=50,
    #                            min_length=2,
    #                            required=True,
    #                            error_messages={'required': "UI页面元素名称不能为空"})

    ui_page_element = forms.CharField(max_length=2000,
                               min_length=2,
                               required=False,
                               error_messages={'required': "页面元素超过2000字符"})

    ui_project_id = forms.CharField(required=False)

    # ui_page_id = forms.CharField(required=False)

    ui_element_positioning_id = forms.CharField(required=False)

