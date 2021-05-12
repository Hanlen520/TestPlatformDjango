# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 11:42
# @Author  : wangyinghao
# @FileName: ui_element_operation_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success, response_failed
from automated_main.models.ui_automation.ui_element_operation import UIElementsOperation
import arrow
from django.core.paginator import Paginator


class UiElementOperationListView(View):

    def get(self, request, *args, **kwargs):
        '''
        代表获取所有元素操作
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ui_element_operation = UIElementsOperation.objects.all()
        ui_element_operation_list = []

        for element_operation in ui_element_operation:
            _tz = 'Asia/Shanghai'
            element_operation_dict = {
                "id": element_operation.id,
                "elements_operation_name": element_operation.elements_operation_name,
                "elements_operation_title": element_operation.elements_operation_title,
                "elements_operation_describe": element_operation.elements_operation_describe,
                "updata_time": arrow.get(element_operation.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(element_operation.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss')
            }
            print(element_operation.create_time)
            ui_element_operation_list.append(element_operation_dict)

        return response_success(ui_element_operation_list)

