# -*- coding: utf-8 -*-
# @Time    : 2020/6/28 18:06
# @Author  : wangyinghao
# @FileName: project_views.py
# @Software: PyCharm
from django.views.generic import View
import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from automated_main.utils.http_format import response_success, response_failed
from automated_main.utils.log import default_log
from automated_main.exception.my_exception import MyException
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from automated_main.form.user import UserForm


class UsersView(View):

    def get(self, request, *args, **kwargs):
        '''
        代表登录
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        form = UserForm(request.GET)
        result = form.is_valid()
        if not result:
            default_log.error(form.errors.as_json())
            raise MyException()
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])

        if user:
            # 登录持久化，生成session
            login(request, user)
            return response_success("登录成功")
        else:
            raise MyException(message="登录失败")

    def post(self, request, *args, **kwargs):
        '''
        代表的注册
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        body = request.body
        data = json.loads(body)

        form = UserForm(data)
        result = form.is_valid()
        if not result:
            default_log.error(form.errors.as_json())
            raise MyException()

        if User.objects.filter(username=form.cleaned_data["username"]).exists():
            raise MyException(message="用户已存在")

        # result = User.objects.create_user(username=data["username"], password=data["password"])
        user = User.objects.create_user(username=form.cleaned_data["username"], password=form.cleaned_data["password"])

        if user:
            login(request, user)
            return response_success("注册成功")
        else:
            raise MyException(message="注册失败")

    def delete(self, request, *args, **kwargs):
        '''
        代表的注销
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        logout(request)
        return response_success("注销成功")

