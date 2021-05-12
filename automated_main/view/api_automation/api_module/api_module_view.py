# -*- coding: utf-8 -*-
# @Time    : 2021/3/3 11:02
# @Author  : wangyinghao
# @FileName: api_module_view.py
# @Software: PyCharm

from django.views.generic import View
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.utils.log import default_log
from automated_main.exception.my_exception import MyException
from automated_main.models.api_automation.api_module import APIModule
import arrow
from automated_main.form.api_module import ApiModuleForm


class ApiModuleView(View):

    def get(self, request, api_module_id, *args, **kwargs):
        '''
        代表获取单个API模块
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        api_module = APIModule.objects.filter(id=api_module_id).first()

        if api_module is None:
            return response_success()
        else:
            return response_success(model_to_dict(api_module))

    def post(self, request, api_module_id, *args, **kwargs):
        '''
        代表更改页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        api_module = APIModule.objects.filter(id=api_module_id).first()
        if api_module is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = ApiModuleForm(data)

        if form.is_valid():
            APIModule.objects.filter(id=api_module_id).update(**form.cleaned_data)
            return response_success("编辑API模块成功")
        else:
            raise MyException()

    def delete(self, request, api_module_id, *args, **kwargs):
        '''
        代表删除单独模块
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        APIModule.objects.filter(id=api_module_id).delete()
        return response_success("删除模块成功")

    def put(self, request, *args, **kwargs):
        '''
        代表创建模块
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = ApiModuleForm(data)

        if form.is_valid():

            APIModule.objects.create(**form.cleaned_data)
            return response_success("创建成功")
        else:
            raise MyException(message="创建失败")


class ApiProjectModuleView(View):

    def get(self, request, api_project_id, *args, **kwargs):
        '''
        获取 单个API项目中包含得所有模块
        :param request:
        :param api_project_id:api项目id
        :param args:
        :param kwargs:
        :return:
        '''
        api_module = APIModule.objects.filter(api_project_id=api_project_id)

        api_module_list = []
        for api_modules in api_module:
            _tz = 'Asia/Shanghai'
            api_module_dict = {
                "id": api_modules.id,
                "api_project_name": api_modules.api_project.api_project_name,
                "api_module_name": api_modules.api_module_name,
                "api_module_describe": api_modules.api_module_describe,
                "updata_time": arrow.get(api_modules.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(api_modules.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
            }
            api_module_list.append(api_module_dict)

        if api_module is None:
            return response_success()
        else:
            return response_success(api_module_list)



