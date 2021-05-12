# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 18:46
# @Author  : wangyinghao
# @FileName: ui_test_case_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success, response_failed
from automated_main.models.ui_automation.ui_test_case import UITestCase
import arrow


class UITestCaseListView(View):

    def get(self, request, ui_project_id, *args, **kwargs):
        '''
        代表获取所有UI测试用例元素
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ui_test_case = UITestCase.objects.filter(ui_project_id=ui_project_id)
        ui_test_case_list = []

        for ui_test_cases in ui_test_case:
            _tz = 'Asia/Shanghai'
            ui_test_cases_dict = {
                "id": ui_test_cases.id,
                "ui_test_case_name": ui_test_cases.ui_test_case_name,
                "ui_project_id": ui_test_cases.ui_project.id,
                "ui_project_name": ui_test_cases.ui_project.ui_project_name,
                "updata_time": arrow.get(ui_test_cases.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(ui_test_cases.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss')
            }
            print(ui_test_cases.create_time)
            ui_test_case_list.append(ui_test_cases_dict)

        return response_success(ui_test_case_list)
