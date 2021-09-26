# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 15:27
# @Author  : wangyinghao
# @FileName: api_environment_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success
from automated_main.models.api_automation.api_environment import APIEnvironment
import arrow


class ApiEnvironmentListView(View):

    def get(self, request, *args, **kwargs):
        """
        代表获取所有Api环境列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        api_environment = APIEnvironment.objects.all()
        api_environment_list = []

        for api_environments in api_environment:
            api_environment_dict = {
                "id": api_environments.id,
                "api_environment_name": api_environments.api_environment_name,
                "api_title": api_environments.api_title,
                "api_environment_describe": api_environments.api_environment_describe,
                "updata_time": arrow.get(str(api_environments.updata_time)).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(str(api_environments.create_time)).format('YYYY-MM-DD HH:mm:ss'),

            }
            api_environment_list.append(api_environment_dict)

        return response_success(api_environment_list)
