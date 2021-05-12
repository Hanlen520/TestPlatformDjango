# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 10:05
# @Author  : wangyinghao
# @FileName: ui_test_task_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success, response_failed
from automated_main.models.ui_automation.ui_test_task import UITestTask
import arrow


class UITestTaskListView(View):

    def get(self, request, ui_project_id, *args, **kwargs):
        '''
        代表获取所有UI测试任务
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        ui_task = UITestTask.objects.filter(ui_project_id=ui_project_id).order_by('id')
        ui_task_list = []
        for ui_tasks in ui_task:
            _tz = 'Asia/Shanghai'
            if ui_tasks.status == 0:
                status = "未执行"
            elif ui_tasks.status == 1:
                status = "执行中"
            elif ui_tasks.status == 2:
                status = "已完成"
            ui_task_dict = {
                "id": ui_tasks.id,
                "ui_test_task_name": ui_tasks.ui_test_task_name,
                "describe": ui_tasks.describe,
                "cases": ui_tasks.cases,
                "ui_project_name": ui_tasks.ui_project.ui_project_name,
                "status": status,
                "updata_time": arrow.get(ui_tasks.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(ui_tasks.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),

            }
            print(ui_tasks.create_time)
            ui_task_list.append(ui_task_dict)

        return response_success(ui_task_list)
