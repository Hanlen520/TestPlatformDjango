# -*- coding: utf-8 -*-
# @Time    : 2020/12/9 13:32
# @Author  : wangyinghao
# @FileName:
# @Software: PyCharm
from django.views.generic import View
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.utils.log import default_log
from automated_main.exception.my_exception import MyException
from automated_main.models.ui_automation.ui_project import UIProject
from automated_main.form.ui_project import UiProjectForm
import datetime


class UiProjectView(View):

    def get(self, request, ui_project_id, *args, **kwargs):
        '''
        代表获取单个项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ui_project = UIProject.objects.filter(id=ui_project_id).first()
        if ui_project is None:
            return response_success()
        else:
            return response_success(model_to_dict(ui_project))

    def post(self, request, ui_project_id, *args, **kwargs):
        '''
        代表更改项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ui_project = UIProject.objects.filter(id=ui_project_id).first()
        if ui_project is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = UiProjectForm(data)

        if form.is_valid():
            # UIProject.objects.filter(id=ui_project_id).update(ui_project_name=form.cleaned_data["ui_project_name"],
            #                                                   describe=form.cleaned_data["describe"])
            UIProject.objects.filter(id=ui_project_id).update(**form.cleaned_data)
            return response_success("编辑UI项目成功")
        else:
            raise MyException()

    def delete(self, request, ui_project_id, *args, **kwargs):
        '''
        代表删除单独项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        UIProject.objects.filter(id=ui_project_id).delete()
        return response_success()

    def put(self, request, *args, **kwargs):
        '''
        代表创建项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = UiProjectForm(data)

        if form.is_valid():
            # UIProject.objects.filter(id=ui_project_id).update(ui_project_name=form.cleaned_data["ui_project_name"],
            #                                                   describe=form.cleaned_data["describe"])
            UIProject.objects.create(**form.cleaned_data)
            return response_success()
        else:
            raise MyException()

    def post(self, request, ui_project_id, *args, **kwargs):
        '''
        代表编辑项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ui_project = UIProject.objects.filter(id=ui_project_id).first()
        if ui_project is None:
            return response_success()

        body = request.body

        if not body:
            return response_success()
        data = json.loads(body)

        form = UiProjectForm(data)
        print(form)
        if form.is_valid():
            UIProject.objects.filter(id=ui_project_id).update(**form.cleaned_data, updata_time=datetime.datetime.now())
            return response_success()
        else:
            raise MyException()
