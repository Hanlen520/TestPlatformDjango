# -*- coding: utf-8 -*-
# @Time    : 2021/3/2 18:41
# @Author  : wangyinghao
# @FileName: api_project_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success
from automated_main.models.api_automation.api_project import APIProject
import arrow


class ApiProjectListView(View):

    def get(self, request, *args, **kwargs):
        '''
        代表获取所有api项目列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        data = request.GET
        size = int(data.get('size', 10))
        page = int(data.get('page', 1))
        api_projects = APIProject.objects.all()
        api_project_list = []

        for api_project in api_projects:
            _tz = 'Asia/Shanghai'
            api_project_dict = {
                "id": api_project.id,
                "api_project_name": api_project.api_project_name,
                "describe": api_project.describe,
                "updata_time": arrow.get(api_project.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(api_project.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
            }
            print(api_project.create_time)
            api_project_list.append(api_project_dict)

        return response_success(api_project_list)

