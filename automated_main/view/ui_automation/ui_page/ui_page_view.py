# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 18:07
# @Author  : wangyinghao
# @FileName: ui_page_view.py
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
import arrow
from automated_main.form.ui_page import UiPageForm


class UiPageView(View):

    def get(self, request, ui_page_id, *args, **kwargs):
        '''
        代表获取单个UI页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ui_page = UIPage.objects.filter(id=ui_page_id).first()

        if ui_page is None:
            return response_success()
        else:
            return response_success(model_to_dict(ui_page))

    def post(self, request, ui_page_id, *args, **kwargs):
        '''
        代表更改页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        ui_page = UIPage.objects.filter(id=ui_page_id).first()
        if ui_page is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = UiPageForm(data)

        if form.is_valid():
            UIPage.objects.filter(id=ui_page_id).update(**form.cleaned_data)
            return response_success("编辑UI页面成功")
        else:
            raise MyException()

    def delete(self, request, ui_page_id, *args, **kwargs):
        '''
        代表删除单独页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        UIPage.objects.filter(id=ui_page_id).delete()
        return response_success("删除页面成功")

    def put(self, request, *args, **kwargs):
        '''
        代表创建页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = UiPageForm(data)

        if form.is_valid():
            # UIProject.objects.filter(id=ui_project_id).update(ui_project_name=form.cleaned_data["ui_project_name"],
            #                                                   describe=form.cleaned_data["describe"])
            UIPage.objects.create(**form.cleaned_data)
            return response_success("创建成功")
        else:
            raise MyException(message="创建失败")


class UiProjectPageView(View):

    def get(self, request, ui_project_id, *args, **kwargs):
        '''
        获取 单个UI项目中包含得所有页面
        :param request:
        :param ui_project_id:
        :param args:
        :param kwargs:
        :return:
        '''
        ui_page = UIPage.objects.filter(ui_project_id=ui_project_id)

        ui_page_list = []
        for pages in ui_page:
            _tz = 'Asia/Shanghai'
            page_dict = {
                "id": pages.id,
                "ui_project_name": pages.ui_project.ui_project_name,
                "ui_page_name": pages.ui_page_name,
                "ui_page_describe": pages.ui_page_describe,
                "updata_time": arrow.get(pages.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(pages.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
            }
            ui_page_list.append(page_dict)

        if ui_page is None:
            return response_success()
        else:
            return response_success(ui_page_list)



