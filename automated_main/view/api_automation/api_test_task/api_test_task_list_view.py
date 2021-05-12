# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 14:05
# @Author  : wangyinghao
# @FileName: api_test_task_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success, response_failed
from automated_main.models.api_automation.api_test_task import APITestTask
import arrow


class ApiTestTaskListView(View):

    def get(self, request, api_project_id, *args, **kwargs):
        """
        代表获取所有API测试任务
        :param request:
        :param api_project_id: API项目id
        :param args:
        :param kwargs:
        :return:
        """
        api_task = APITestTask.objects.filter(api_project_id=api_project_id).order_by('id')
        api_task_list = []
        for api_tasks in api_task:
            _tz = 'Asia/Shanghai'
            if api_tasks.status == 0:
                status = "未执行"
            elif api_tasks.status == 1:
                status = "执行中"
            elif api_tasks.status == 2:
                status = "已完成"
            api_task_dict = {
                "id": api_tasks.id,
                "api_project_name": api_tasks.api_project.api_project_name,
                "api_test_task_name": api_tasks.api_test_task_name,
                "describe": api_tasks.describe,
                "cases": api_tasks.cases,
                "ui_project_name": api_tasks.api_project.api_project_name,
                "status": status,
                "updata_time": arrow.get(api_tasks.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(api_tasks.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),

            }
            print(api_tasks.create_time)
            api_task_list.append(api_task_dict)

        return response_success(api_task_list)
