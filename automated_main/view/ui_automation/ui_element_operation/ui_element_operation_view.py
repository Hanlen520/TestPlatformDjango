# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 11:42
# @Author  : wangyinghao
# @FileName: ui_element_operation_view.py
# @Software: PyCharm
from django.views.generic import View
import json
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.exception.my_exception import MyException
from automated_main.models.ui_automation.ui_element_operation import UIElementsOperation
from automated_main.form.ui_element_operation import UIElementsOperationForm


class UIElementOperationView(View):

    def get(self, request, element_operation_id, *args, **kwargs):
        """
        代表获取单个元素操作
        :param request:
        :param element_operation_id:
        :param args:
        :param kwargs:
        :return:
        """

        element_operation = UIElementsOperation.objects.filter(id=element_operation_id).first()
        if element_operation is None:
            return response_success()
        else:
            return response_success(model_to_dict(element_operation))

    def post(self, request, element_operation_id, *args, **kwargs):
        """
        代表更改元素操作
        :param request:
        :param element_operation_id:
        :param args:
        :param kwargs:
        :return:
        """

        element_operation = UIElementsOperation.objects.filter(id=element_operation_id).first()
        if element_operation is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = UIElementsOperationForm(data)

        if form.is_valid():
            # UIProject.objects.filter(id=ui_project_id).update(ui_project_name=form.cleaned_data["ui_project_name"],
            #                                                   describe=form.cleaned_data["describe"])
            UIElementsOperation.objects.filter(id=element_operation_id).update(**form.cleaned_data)
            return response_success("编辑元素操作成功")
        else:
            raise MyException()

    def delete(self, request, element_operation_id, *args, **kwargs):
        """
        代表删除单独元素操作
        :param request:
        :param element_operation_id:
        :param args:
        :param kwargs:
        :return:
        """

        UIElementsOperation.objects.filter(id=element_operation_id).delete()
        return response_success("删除元素操作成功")

    def put(self, request, *args, **kwargs):
        """
        代表创建元素操作
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = UIElementsOperationForm(data)

        if form.is_valid():
            UIElementsOperation.objects.create(**form.cleaned_data)
            return response_success("创建元素操作成功")
        else:
            raise MyException()

