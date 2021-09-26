# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 18:07
# @Author  : wangyinghao
# @FileName: ui_page_list_view.py
# @Software: PyCharm
from django.views.generic import View
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.utils.log import default_log
from automated_main.exception.my_exception import MyException
from automated_main.models.ui_automation.ui_page import UIPage
from automated_main.form.ui_project import UiProjectForm
from automated_main.utils.calc import CalcUtils
from datetime import datetime
import arrow


class UiPageListView(View):

    def get(self, request, *args, **kwargs):
        """
        代表获取所有UI页面列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        data = request.GET
        size = int(data.get('size', 10))
        page = int(data.get('page', 1))
        ui_page = UIPage.objects.all()
        ui_page_list = []

        for ui_pages in ui_page:
            page_dict = {
                "id": ui_pages.id,
                "ui_page_name": ui_pages.ui_page_name,
                "ui_page_describe": ui_pages.ui_page_describe,
                "updata_time": arrow.get(str(ui_pages.updata_time)).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(str(ui_pages.create_time)).format('YYYY-MM-DD HH:mm:ss'),
                "ui_project_name": ui_pages.ui_project.ui_project_name
            }
            ui_page_list.append(page_dict)

        return response_success(ui_page_list)

