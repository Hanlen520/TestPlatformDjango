# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/27 17:46
@Auth ： WangYingHao
@File ：performance_script_list_view.py
@IDE ：PyCharm

"""

from django.views.generic import View
from automated_main.utils.http_format import response_success, response_failed
from automated_main.models.performance_test.performance_script import PerformanceScript
import arrow


class PerformanceScriptListView(View):

    def get(self, request, *args, **kwargs):
        """
        代表获取所有项目-性能脚本列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        data = request.GET
        size = int(data.get('size', 10))
        page = int(data.get('page', 1))
        performance_script = PerformanceScript.objects.all()
        performance_script_list = []

        for performance_scripts in performance_script:
            performance_script_dict = {
                "id": performance_scripts.id,
                "performance_project": performance_scripts.performance_project.performance_project_name,
                "performance_script_name": performance_scripts.performance_script_name,
                "updata_time": arrow.get(str(performance_scripts.updata_time)).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(str(performance_scripts.create_time)).format('YYYY-MM-DD HH:mm:ss')
            }
            performance_script_list.append(performance_script_dict)

        return response_success(performance_script_list)


