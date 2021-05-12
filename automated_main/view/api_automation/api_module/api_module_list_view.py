# -*- coding: utf-8 -*-
# @Time    : 2021/3/3 11:02
# @Author  : wangyinghao
# @FileName: api_module_list_view.py
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
from automated_main.form.api_module import ApiModuleForm
from automated_main.utils.calc import CalcUtils
from datetime import datetime
import arrow


class ApiModuleListView(View):

    def get(self, request, *args, **kwargs):
        """
        代表获取所有Api模块列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        data = request.GET
        size = int(data.get('size', 10))
        page = int(data.get('page', 1))
        api_module = APIModule.objects.all()
        api_module_list = []

        for api_modules in api_module:
            _tz = 'Asia/Shanghai'
            api_module_dict = {
                "id": api_modules.id,
                "api_module_name": api_modules.ui_page_name,
                "api_module_describe": api_modules.ui_page_describe,
                "updata_time": arrow.get(api_modules.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(api_modules.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "api_project_name": api_modules.ui_project.ui_project_name
            }
            api_module_list.append(api_module_dict)

        return response_success(api_module_list)

