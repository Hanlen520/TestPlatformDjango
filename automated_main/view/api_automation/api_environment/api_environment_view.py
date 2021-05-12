# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 15:28
# @Author  : wangyinghao
# @FileName: api_environment_view.py
# @Software: PyCharm
from django.views.generic import View
import json
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success
from automated_main.exception.my_exception import MyException
from automated_main.models.api_automation.api_environment import APIEnvironment
from automated_main.form.api_environment import ApiEnvironmentForm


class ApiEnvironmentView(View):

    def get(self, request, api_environment_id, *args, **kwargs):
        '''
        代表获取单个API环境
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        api_environment = APIEnvironment.objects.filter(id=api_environment_id).first()

        if api_environment is None:
            return response_success()
        else:
            return response_success(model_to_dict(api_environment))

    def post(self, request, api_environment_id, *args, **kwargs):
        '''
        代表更改API环境
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        api_environment = APIEnvironment.objects.filter(id=api_environment_id).first()
        if api_environment is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = ApiEnvironmentForm(data)

        if form.is_valid():
            APIEnvironment.objects.filter(id=api_environment_id).update(**form.cleaned_data)
            return response_success("编辑API环境成功")
        else:
            raise MyException()

    def delete(self, request, api_environment_id, *args, **kwargs):
        '''
        代表删除单独API环境
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        APIEnvironment.objects.filter(id=api_environment_id).delete()
        return response_success("删除API环境成功")

    def put(self, request, *args, **kwargs):
        '''
        代表创建API环境
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = ApiEnvironmentForm(data)

        if form.is_valid():

            APIEnvironment.objects.create(**form.cleaned_data)
            return response_success("创建成功")
        else:
            raise MyException(message="创建失败")
