# -*- coding: utf-8 -*-
# @Time    : 2021/3/2 18:41
# @Author  : wangyinghao
# @FileName: performance_project_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success
from automated_main.models.performance_test.performance_project import PerformanceProject
import arrow


class PerformanceProjectListView(View):

    def get(self, request, *args, **kwargs):
        """
        代表获取所有api项目列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        data = request.GET
        size = int(data.get('size', 10))
        page = int(data.get('page', 1))
        performance_projects = PerformanceProject.objects.all()
        performance_project_list = []

        for performance_project in performance_projects:
            api_project_dict = {
                "id": performance_project.id,
                "performance_project_name": performance_project.performance_project_name,
                "describe": performance_project.describe,
                "updata_time": arrow.get(str(performance_project.updata_time)).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(str(performance_project.create_time)).format('YYYY-MM-DD HH:mm:ss'),
            }
            performance_project_list.append(api_project_dict)

        return response_success(performance_project_list)

