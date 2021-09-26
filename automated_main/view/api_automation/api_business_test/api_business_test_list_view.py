# -*- coding: utf-8 -*-
# @Time    : 2021/4/14 18:59
# @Author  : wangyinghao
# @FileName: api_business_test_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success
from automated_main.models.api_automation.api_business_test import ApiBusinessTest
import arrow


class ApiBusinessTestListView(View):

    def get(self, request, api_project_id, *args, **kwargs):
        """
        代表获取该项目下所有API业务测试
        :param request:
        :param api_project_id: api项目id
        :param args:
        :param kwargs:
        :return:
        """

        api_business_case = ApiBusinessTest.objects.filter(api_project_id=api_project_id)
        api_business_case_list = []

        for api_business_cases in api_business_case:
            ui_test_cases_dict = {
                "id": api_business_cases.id,
                "api_business_test_name": api_business_cases.api_business_test_name,
                "api_project_id": api_business_cases.api_project.id,
                "api_project_name": api_business_cases.api_project.api_project_name,
                "update_time": arrow.get(str(api_business_cases.updata_time)).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(str(api_business_cases.create_time)).format('YYYY-MM-DD HH:mm:ss')
            }
            api_business_case_list.append(ui_test_cases_dict)

        return response_success(api_business_case_list)
