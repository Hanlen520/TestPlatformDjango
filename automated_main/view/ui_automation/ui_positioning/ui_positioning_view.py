# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 18:12
# @Author  : wangyinghao
# @FileName: ui_positioning_view.py
# @Software: PyCharm
from django.views.generic import View
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.utils.log import default_log
from automated_main.exception.my_exception import MyException
from automated_main.models.ui_automation.ui_element_positioning import UIPositioning
from automated_main.form.ui_element_positioning import UiPositioningForm
import datetime


class UIPositioningView(View):

    def get(self, request, element_positioning_id, *args, **kwargs):
        """
        代表获取单个元素定位
        :param request:
        :param element_positioning_id:
        :param args:
        :param kwargs:
        :return:
        """

        element_operation = UIPositioning.objects.filter(id=element_positioning_id).first()
        if element_operation is None:
            return response_success()
        else:
            return response_success(model_to_dict(element_operation))

    def post(self, request, element_positioning_id, *args, **kwargs):
        """
        :param request:
        :param element_positioning_id:
        :param args:
        :param kwargs:
        :return:
        """

        element_positioning = UIPositioning.objects.filter(id=element_positioning_id).first()
        if element_positioning is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = UiPositioningForm(data)

        if form.is_valid():
            UIPositioning.objects.filter(id=element_positioning_id).update(**form.cleaned_data)
            return response_success("编辑UI项目成功")
        else:
            raise MyException()

    def delete(self, request, element_positioning_id, *args, **kwargs):
        """
        代表删除单独元素定位
        :param request:
        :param element_positioning_id:
        :param args:
        :param kwargs:
        :return:
        """

        UIPositioning.objects.filter(id=element_positioning_id).delete()
        return response_success("删除元素定位成功")

    def put(self, request, *args, **kwargs):
        """
        代表创建元素定位
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = UiPositioningForm(data)

        if form.is_valid():
            UIPositioning.objects.create(**form.cleaned_data)
            return response_success("创建元素定位成功")
        else:
            raise MyException()

    def post(self, request, element_positioning_id, *args, **kwargs):
        """
        代表编辑元素定位
        :param request:
        :param element_positioning_id:
        :param args:
        :param kwargs:
        :return:
        """

        element_operation = UIPositioning.objects.filter(id=element_positioning_id).first()
        if element_operation is None:
            return response_success()

        body = request.body

        if not body:
            return response_success()
        data = json.loads(body)

        form = UiPositioningForm(data)
        if form.is_valid():
            UIPositioning.objects.filter(id=element_positioning_id).update(**form.cleaned_data, updata_time=datetime.datetime.now())
            return response_success("编辑元素定位成功")
        else:
            raise MyException()
