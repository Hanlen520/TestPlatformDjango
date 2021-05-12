# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 18:39
# @Author  : wangyinghao
# @FileName: ui_page.py
# @Software: PyCharm
from django import forms


class UiPageForm(forms.Form):
    ui_page_name = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "UI页面名称不能为空"})

    ui_page_describe = forms.CharField(max_length=2000,
                               min_length=2,
                               required=False,
                               error_messages={'required': "描述超过2000字符"})

    ui_project_id = forms.CharField(required=False)

