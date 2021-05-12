# -*- coding: utf-8 -*-
# @Time    : 2020/11/12 11:27
# @Author  : wangyinghao
# @FileName: user.py
# @Software: PyCharm
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "用户名不能为空"})

    password = forms.CharField(max_length=50,
                               min_length=2,
                               required=True,
                               error_messages={'required': "密码不能为空"})

