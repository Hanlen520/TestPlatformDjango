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
from automated_main.models.ui_automation.ui_test_task import UITestTask, UITestResult, UITestResultAssociated
from automated_main.models.ui_automation.ui_project import UIProject
from automated_main.models.ui_automation.ui_test_case import UITestCase
from automated_main.form.ui_test_task import UiTestTaskForm
from automated_main.view.ui_automation.ui_test_task.extend.task_thread import TaskThread
import arrow
from django.http import FileResponse
import os
from AutomatedTestPlatform import settings
import logging

logger = logging.getLogger('django')

from functools import reduce


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

        form = UiTestTaskForm(data)

        if form.is_valid():
            if data['ui_test_task_id'] == 0:
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
        task.status = 1
        task.save()

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
                "ui_error_total_number": i.ui_error_total_number,
                "ui_total_number": i.ui_total_number,
                "ui_successful_total_number": i.ui_successful_total_number,
                "ui_test_script": i.ui_test_script,
                "create_time": arrow.get(str(i.create_time, )).format('YYYY-MM-DD HH:mm:ss'),
                "updata_time": arrow.get(str(i.updata_time)).format('YYYY-MM-DD HH:mm:ss')
            }
            data.append(result)
        return response_success({'status': 10102, 'data': data})

    def delete(self, request, ui_test_task_id, ui_test_result_id, *args, **kwargs):
        """
        删除单独测试报告列表
        :param ui_test_result_id:
        :param request:
        :param ui_test_task_id:
        :param args:
        :param kwargs:
        :return:
        """
        if ui_test_task_id == "":
            return response_failed({"status": 10102, "message": "ui_test_task_id不能为空"})

        if ui_test_result_id == "":
            return response_failed({"status": 10102, "message": "ui_test_result_id不能为空"})

        UITestResult.objects.get(ui_task_id=ui_test_task_id, id=ui_test_result_id).delete()

        return response_success("删除UI测试任务成功")


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
        ui_result = UITestResultAssociated.objects.filter(ui_result_id=ui_test_result_id)

        single_case_results = []

        for single_case in ui_result:
            single_case_dict = {
                "id": single_case.id,
                "ui_test_case_name": single_case.ui_test_case_name,
                "ui_error": single_case.ui_error,
                "ui_successful": single_case.ui_successful,
            }
            single_case_results.append(single_case_dict)

        ui_error_case_list = []

        for ui_error_case in single_case_results:
            if int(ui_error_case['ui_error']) == int(1):
                ui_error_case_list.append(ui_error_case)

        for remove_case in ui_error_case_list:
            i = 0
            while i < len(single_case_results):
                if remove_case['ui_test_case_name'] == single_case_results[i]["ui_test_case_name"] and int(single_case_results[i]['ui_error']) == int(0):
                    single_case_results.pop(i)
                    i -= 1

                i += 1

        # 用于存储去重后的list-最终获取数据
        new_data = []

        # 用于存储当前已有的值
        values = []
        for d in single_case_results:
            if d["ui_test_case_name"] not in values:
                new_data.append(d)
                values.append(d["ui_test_case_name"])

        ui_total_number = len(new_data)

        ui_error_total_number = UITestResultAssociated.objects.filter(ui_result_id=ui_test_result_id,
                                                                      ui_error=1).count()

        ui_successful_total_number = ui_total_number - ui_error_total_number
        case_result_total = [ui_successful_total_number, ui_error_total_number]

        return response_success({'status': 10102, "case_result_total": case_result_total, "data": new_data})

    def get(self, request, ui_test_abnormal_result_id, *args, **kwargs):
        """
        获取异常测试报告
        :param request:
        :param ui_test_abnormal_result_id:
        :param args:
        :param kwargs:
        :return:
        """
        if ui_test_abnormal_result_id == "":
            return response_failed({"status": 10102, "message": "ui_test_abnormal_result_id不能为空"})
        ui_test_abnormal = UITestResultAssociated.objects.get(id=ui_test_abnormal_result_id)

        return response_success({"ui_test_abnormal": ui_test_abnormal.abnormal})


class DownloadWebScript(View):

    def get(self, request, ui_test_result_id, *args, **kwargs):
        """
        下载web自动化脚本
        :param request:
        :param ui_test_result_id:
        :param args:
        :param kwargs:
        :return:
        """
        if ui_test_result_id == "":
            return response_failed({"status": 10102, "message": "ui_test_abnormal_result_id不能为空"})
        ui_test_result = UITestResult.objects.get(id=ui_test_result_id)

        ENV_PROFILE = os.getenv("ENV")
        if ENV_PROFILE == "SERVER":
            file = open('/home/Web_Script/' + str(ui_test_result.ui_test_script), 'rb')
        elif ENV_PROFILE == "1":
            file = open(os.path.join(settings.WEB_ROOT, str(ui_test_result.ui_test_script)), 'rb')

        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;' + ' filename=' + str(ui_test_result.ui_test_script)
        return response


class DownloadWebScriptTemplate(View):

    def get(self, request, *args, **kwargs):
        """
        下载web自动化脚本模板
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        print(settings.WEB_TEMPLATE)
        logger.info("web脚本地址：" + settings.WEB_TEMPLATE)
        file = open(settings.WEB_TEMPLATE, 'rb')

        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;' + ' filename=' + "TestScriptTemplate.py"
        return response





