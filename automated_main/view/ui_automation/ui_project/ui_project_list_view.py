# -*- coding: utf-8 -*-
# @Time    : 2020/12/9 15:27
# @Author  : wangyinghao
# @FileName: ui_project_list_view.py
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
from automated_main.utils.calc import CalcUtils
from datetime import datetime
import arrow


class UiProjectListView(View):

    def get(self, request, *args, **kwargs):
        '''
        代表获取所有项目列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        data = request.GET
        size = int(data.get('size', 10))
        page = int(data.get('page', 1))
        ui_projects = UIProject.objects.all()
        ui_project_list = []

        for ui_project in ui_projects:
            _tz = 'Asia/Shanghai'
            project_dict = {
                "id": ui_project.id,
                "ui_project_name": ui_project.ui_project_name,
                "describe": ui_project.describe,
                "updata_time": arrow.get(ui_project.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(ui_project.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
            }
            print(ui_project.create_time)
            ui_project_list.append(project_dict)

        return response_success(ui_project_list)

