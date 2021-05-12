# -*- coding: utf-8 -*-
# @Time    : 2021/3/2 18:41
# @Author  : wangyinghao
# @FileName: api_project_view.py
# @Software: PyCharm

from django.views.generic import View
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.utils.log import default_log
from automated_main.exception.my_exception import MyException
from automated_main.models.api_automation.api_project import APIProject
from automated_main.form.api_project import ApiProjectForm
import datetime


class ApiProjectView(View):

    def get(self, request, api_project_id, *args, **kwargs):
        '''
        代表获取单个API项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        api_project = APIProject.objects.filter(id=api_project_id).first()
        if api_project is None:
            return response_success()
        else:
            return response_success(model_to_dict(api_project))

    def post(self, request, api_project_id, *args, **kwargs):
        """
        代表更改API项目
        :param request:
        :param api_project_id:
        :param args:
        :param kwargs:
        :return:
        """

        api_project = APIProject.objects.filter(id=api_project_id).first()
        if api_project is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = ApiProjectForm(data)

        if form.is_valid():

            APIProject.objects.filter(id=api_project_id).update(**form.cleaned_data)
            return response_success("编辑UI项目成功")
        else:
            raise MyException()

    def delete(self, request, api_project_id, *args, **kwargs):
        '''
        代表删除单独API项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        APIProject.objects.filter(id=api_project_id).delete()
        return response_success()

    def put(self, request, *args, **kwargs):
        '''
        代表创建API项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = ApiProjectForm(data)

        if form.is_valid():
            APIProject.objects.create(**form.cleaned_data)
            return response_success()
        else:
            raise MyException()

    # def post(self, request, api_project_id, *args, **kwargs):
    #     '''
    #     代表编辑项目
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     '''
    #
    #     api_project = APIProject.objects.filter(id=api_project_id).first()
    #     if api_project is None:
    #         return response_success()
    #
    #     body = request.body
    #
    #     if not body:
    #         return response_success()
    #     data = json.loads(body)
    #
    #     form = ApiProjectForm(data)
    #     print(form)
    #     if form.is_valid():
    #         APIProject.objects.filter(id=api_project_id).update(**form.cleaned_data, updata_time=datetime.datetime.now())
    #         return response_success()
    #     else:
    #         raise MyException()
