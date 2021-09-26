# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/18 11:24
@Auth ： WangYingHao
@File ：system_home_page_list_view.py
@IDE ：PyCharm

"""

from django.views.generic import View
from automated_main.utils.http_format import response_success, response_failed
from automated_main.models.api_automation.api_test_case import ApiTestCase
from automated_main.models.ui_automation.ui_test_case import UITestCase
from automated_main.models.performance_test.performance_script import PerformanceScript

import arrow


class SystemHomePageListView(View):

    def get(self, request, *args, **kwargs):
        """
        代表获取所有项目测试用例
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        api_test_case = ApiTestCase.objects.all()
        api_test_case_number = len(api_test_case)

        ui_test_case = UITestCase.objects.all()
        ui_test_case_number = len(ui_test_case)

        performance_script = PerformanceScript.objects.all()
        performance_script_number = len(performance_script)

        return response_success({"api_test_case_number": api_test_case_number,
                                 "ui_test_case_number": ui_test_case_number,
                                 "performance_script_number": performance_script_number}
                                )
