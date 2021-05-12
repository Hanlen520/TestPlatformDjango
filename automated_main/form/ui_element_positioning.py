# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 18:33
# @Author  : wangyinghao
# @FileName: ui_positioning.py
# @Software: PyCharm
from django import forms


class UiPositioningForm(forms.Form):
    positioning_name = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "定位名称不能为空"})

    locating_method = forms.CharField(max_length=2000,
                               min_length=2,
                               required=False,
                               error_messages={'required': "定位方法不能为空"})

    describe = forms.CharField(max_length=2000,
                               min_length=2,
                               required=False,
                               error_messages={'required': "描述超过2000字符"})

