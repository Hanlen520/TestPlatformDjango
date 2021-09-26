# -*- coding: utf-8 -*-
# @Time    : 2021/3/29 18:58
# @Author  : wangyinghao
# @FileName: api_test_case_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success
from automated_main.models.api_automation.api_test_case import ApiTestCase
import arrow


class ApiTestCaseListView(View):

    def post(self, request, api_module_id, *args, **kwargs):
        """
        :param request:
        :param api_module_id: API模块id
        :param args:
        :param kwargs:
        :return:
        """
        api_test_cases = ApiTestCase.objects.filter(api_module=api_module_id)
        api_test_case_list = []

        for api_test_case in api_test_cases:
            api_test_case_dict = {
                "id": api_test_case.id,
                "api_module_name": api_test_case.api_module.api_module_name,
                "api_test_case_name": api_test_case.api_test_case_name,
                "updata_time": arrow.get(str(api_test_case.updata_time)).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(str(api_test_case.create_time)).format('YYYY-MM-DD HH:mm:ss'),
            }

            api_test_case_list.append(api_test_case_dict)
        return response_success(api_test_case_list)
