# -*- coding: utf-8 -*-
# @Time    : 2021/3/2 18:41
# @Author  : wangyinghao
# @FileName: performance_project_view.py
# @Software: PyCharm

from django.views.generic import View
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.utils.log import default_log
from automated_main.exception.my_exception import MyException
from automated_main.models.performance_test.performance_project import PerformanceProject
from automated_main.form.performance_project import PerformanceProjectForm
import datetime
import logging
logger = logging.getLogger('django')


class PerformanceProjectView(View):

    def get(self, request, performance_project_id, *args, **kwargs):
        """
        获取单独 性能测试项目
        :param request:
        :param performance_project_id: 性能测试项目id
        :param args:
        :param kwargs:
        :return:
        """

        performance_project = PerformanceProject.objects.filter(id=performance_project_id).first()
        if performance_project is None:
            return response_success()
        else:
            return response_success(model_to_dict(performance_project))

    def post(self, request, performance_project_id, *args, **kwargs):
        """
        代表更改性能测试项目
        :param request:
        :param performance_project_id:性能测试项目id
        :param args:
        :param kwargs:
        :return:
        """

        performance_project = PerformanceProject.objects.filter(id=performance_project_id).first()
        if performance_project is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = PerformanceProjectForm(data)

        if form.is_valid():

            PerformanceProject.objects.filter(id=performance_project_id).update(**form.cleaned_data)
            return response_success("编辑UI项目成功")
        else:
            raise MyException()

    def delete(self, request, performance_project_id, *args, **kwargs):
        """
        代表删除单独性能测试项目
        :param request:
        :param performance_project_id: 性能测试项目id
        :param args:
        :param kwargs:
        :return:
        """

        PerformanceProject.objects.filter(id=performance_project_id).delete()
        return response_success()

    def put(self, request, *args, **kwargs):
        """
        代表创建性能测试项目
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = PerformanceProjectForm(data)

        if form.is_valid():
            PerformanceProject.objects.create(**form.cleaned_data)
            return response_success()
        else:
            raise MyException()


