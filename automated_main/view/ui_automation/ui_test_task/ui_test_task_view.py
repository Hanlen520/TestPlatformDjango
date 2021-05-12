# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 10:05
# @Author  : wangyinghao
# @FileName: ui_test_task_view.py
# @Software: PyCharm
from django.views.generic import View
import json
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.exception.my_exception import MyException
from automated_main.models.ui_automation.ui_test_task import UITestTask, UITestResult
from automated_main.models.ui_automation.ui_project import UIProject
from automated_main.models.ui_automation.ui_test_case import UITestCase
from automated_main.form.ui_test_task import UiTestTaskForm
from automated_main.view.ui_automation.ui_test_task.extend.task_thread import TaskThread
# import serializers
from django.core import serializers


class UITestTaskView(View):

    def get(self, request, ui_test_task_id, *args, **kwargs):
        """
        获取单个测试任务
        :param request:
        :param ui_test_task_id:  UI测试任务ID
        :param args:
        :param kwargs:
        :return:
        """
        print(ui_test_task_id)
        ui_test_task = UITestTask.objects.get(id=ui_test_task_id)
        return response_success(model_to_dict(ui_test_task))

    def delete(self, request, ui_test_task_id, *args, **kwargs):
        """
        删除任务
        :param request:
        :param ui_test_task_id: UI测试任务ID
        :param args:
        :param kwargs:
        :return:
        """
        UITestTask.objects.get(id=ui_test_task_id).delete()

        return response_success("删除UI测试任务成功")

    def post(self, request, ui_test_task_id, *args, **kwargs):
        """
        更改UI测试任务
        :param request:
        :param ui_test_task_id: UI测试任务ID
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)
        form = UiTestTaskForm(data)
        if form.is_valid():
            task = UITestTask.objects.get(id=ui_test_task_id)
            task.ui_test_task_name = data['ui_test_task_name']
            task.describe = data['describe']
            task.cases = data['cases']
            task.ui_project_id = data['ui_project_id']
            task.save()
            return response_success("编辑UI测试任务成功")
        else:
            raise MyException()

    def put(self, request, *args, **kwargs):
        """
        创建测试任务
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)
        print(data)

        form = UiTestTaskForm(data)
        print(data['ui_test_task_id'])

        if form.is_valid():
            print(data)
            if data['ui_test_task_id'] == 0:
                print(data)
                UITestTask.objects.create(**form.cleaned_data)
                return response_success("创建UI测试任务成功")
            else:
                return response_success("创建UI测试任务失败")
        else:
            raise MyException()


class GetUiCaseTree(View):

    def get(self, request, ui_project_id, *args, **kwargs):
        """
        获取UI测试用例树形结构
        :param request:
        :param ui_project_id: ui项目id
        :param args:
        :param kwargs:
        :return:
        """
        ui_projects = UIProject.objects.filter(id=ui_project_id)
        data_list = []
        for ui_project in ui_projects:
            ui_project_dict = {
                "ui_project_name": ui_project.ui_project_name,
                "isParent": True
            }
            ui_case_list = []
            ui_test_case = UITestCase.objects.filter(ui_project_id=ui_project.id)
            for ui_test_cases in ui_test_case:
                ui_case_dict = {
                    "ui_test_case_name": ui_test_cases.ui_test_case_name,
                    "isParent": False,
                    "ui_test_cases_id": ui_test_cases.id
                }
                ui_case_list.append(ui_case_dict)

            ui_project_dict["children"] = ui_case_list
            data_list.append(ui_project_dict)
        return response_success(data_list)

    def post(self, request, ui_test_task_id, *args, **kwargs):
        """
        修改UI用例树形结构
        :param request:
        :param ui_test_task_id: ui任务id
        :param args:
        :param kwargs:
        :return:
        """

        if ui_test_task_id == "":
            return MyException("任务id不能为空")
        ui_test_task = UITestTask.objects.get(id=ui_test_task_id)
        ui_case_list_data = json.loads(ui_test_task.cases)
        ui_task_data = {
            "ui_test_task_name": ui_test_task.ui_test_task_name,
            "describe": ui_test_task.describe
        }
        ui_projects = UIProject.objects.all()
        data_list = []
        for ui_project in ui_projects:
            ui_project_dict = {
                "ui_project_name": ui_project.ui_project_name,
                "isParent": True
            }
            ui_case_list = []
            uitest_cases = UITestCase.objects.filter(ui_project_id=ui_project.id)
            for ui_test_case in uitest_cases:
                if ui_test_case.id in ui_case_list_data:
                    ui_case_dict = {
                        "ui_test_case_name": ui_test_case.ui_test_case_name,
                        "ui_test_case_id": ui_test_case.id,
                        "isParent": False,
                        "checked": True,
                    }
                else:
                    ui_case_dict = {
                        "ui_test_case_name": ui_test_case.ui_test_case_name,
                        "ui_test_case_id": ui_test_case.id,
                        "isParent": False,
                        "checked": False,
                    }
                ui_case_list.append(ui_case_dict)

            ui_project_dict["children"] = ui_case_list
            data_list.append(ui_project_dict)
        ui_task_data["cases"] = data_list
        return response_success(ui_task_data)


class PerformUiTask(View):

    def post(self, request, ui_test_task_id, *args, **kwargs):
        """
        执行当前UI任务
        :param request:
        :param ui_test_task_id:
        :param args:
        :param kwargs:
        :return:
        """

        if ui_test_task_id == "":
            return response_failed({"status": 10200, "message": "ui_test_task_id is null"})

        # 1、在执行线程之前，判断当前有没有任务在执行？
        tasks = UITestTask.objects.all()
        for t in tasks:
            if t.status == 1:
                return response_failed({"status": 10200, "message": "当前有任务正在执行！"})

        # 2. 修改任务的状态为：1-执行中
        task = UITestTask.objects.get(id=ui_test_task_id)
        print("第一次", task.status)
        task.status = 1
        task.save()
        print("第二次", task.status)

        # 通过多线程运行测试任务
        TaskThread(ui_test_task_id).run()
        return response_success({"status": 10200, "message": "任务开始执行！"})


class CheckResultList(View):

    def get(self, request, ui_test_task_id, *args, **kwargs):
        """
        查看测试报告列表
        :param request:
        :param ui_test_task_id:
        :param args:
        :param kwargs:
        :return:
        """
        if ui_test_task_id == "":
            return response_failed({"status": 10102, "message": "ui_test_task_id不能为空"})
        r = UITestResult.objects.filter(ui_task_id=ui_test_task_id)
        data = []
        for i in r:
            result = {
                "id": i.id,
                "ui_test_result_name": i.ui_test_result_name,
                "error": i.error,
                "failure": i.failure,
                "skipped": i.skipped,
                "tests": i.tests,
                "run_time": i.run_time,
                "successful": i.successful,
                "result": i.result,
                "create_time": i.create_time
            }
            data.append(result)
        return response_success({'status': 10102, 'data': data})


class CheckResult(View):
    def post(self, request, ui_test_result_id, *args, **kwargs):
        """
        查看测试报告
        :param request:
        :param ui_test_result_id:
        :param args:
        :param kwargs:
        :return:
        """
        if ui_test_result_id == "":
            return response_failed({"status": 10102, "message": "ui_test_task_id不能为空"})
        r = UITestResult.objects.filter(id=ui_test_result_id)
        data = []
        for i in r:
            result = {
                "id": i.id,
                "ui_test_result_name": i.ui_test_result_name,
                "result": i.result,
                "create_time": i.create_time
            }
            data.append(result)
        return response_success({'status': 10102, 'data': data})
