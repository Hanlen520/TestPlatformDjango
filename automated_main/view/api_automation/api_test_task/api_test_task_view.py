# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 14:05
# @Author  : wangyinghao
# @FileName: api_test_task_view.py
# @Software: PyCharm
from django.views.generic import View
import json
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.exception.my_exception import MyException
from automated_main.models.api_automation.api_test_task import APITestTask, APITestResult, APITestResultAssociated
from automated_main.models.api_automation.api_project import APIProject
from automated_main.models.api_automation.api_business_test import ApiBusinessTest
from automated_main.form.api_test_task import ApiTestTaskForm
from automated_main.view.api_automation.api_test_task.extend.task_thread import TaskThread
from django.core import serializers
from django.core.paginator import Paginator


class ApiTestTaskView(View):

    def get(self, request, api_test_task_id, *args, **kwargs):
        """
        获取单个API任务
        :param request:
        :param api_test_task_id: API任务ID
        :param args:
        :param kwargs:
        :return:
        """
        ui_test_task = APITestTask.objects.get(id=api_test_task_id)
        return response_success(model_to_dict(ui_test_task))

    def delete(self, request, api_test_task_id, *args, **kwargs):
        """
        删除API任务
        :param request:
        :param api_test_task_id:任务ID
        :param args:
        :param kwargs:
        :return:
        """
        APITestTask.objects.get(id=api_test_task_id).delete()

        return response_success("删除API任务成功")

    def put(self, request, *args, **kwargs):
        """
        创建API测试任务
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = ApiTestTaskForm(data)

        if form.is_valid():
            print(data)
            if data['api_test_task_id'] == 0:
                print(data)
                APITestTask.objects.create(**form.cleaned_data)
                return response_success("创建API测试任务成功")
            else:
                return response_success("创建API测试任务失败")
        else:
            raise MyException()

    def post(self, request, api_test_task_id, *args, **kwargs):
        """
        更改UI测试任务
        :param request:
        :param api_test_task_id: API测试任务ID
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)
        form = ApiTestTaskForm(data)
        if form.is_valid():
            task = APITestTask.objects.get(id=api_test_task_id)
            task.api_test_task_name = data['api_test_task_name']
            task.describe = data['describe']
            task.cases = data['cases']
            task.api_project_id = data['api_project_id']
            task.save()
            return response_success("编辑API测试任务成功")
        else:
            raise MyException()


class GetApiCaseTree(View):

    def get(self, request, api_project_id, *args, **kwargs):
        """
        获取Api测试用例树形结构
        :param request:
        :param api_project_id:
        :param args:
        :param kwargs:
        :return:
        """
        api_projects = APIProject.objects.filter(id=api_project_id)
        data_list = []
        for api_project in api_projects:
            api_project_dict = {
                "api_project_name": api_project.api_project_name,
                "isParent": True
            }
            api_case_list = []
            api_test_case = ApiBusinessTest.objects.filter(api_project_id=api_project.id)
            for api_test_cases in api_test_case:
                api_case_dict = {
                    "api_test_case_name": api_test_cases.api_business_test_name,
                    "isParent": False,
                    "api_test_cases_id": api_test_cases.id
                }
                api_case_list.append(api_case_dict)

            api_project_dict["children"] = api_case_list
            data_list.append(api_project_dict)
        return response_success(data_list)

    def post(self, request, api_test_task_id, *args, **kwargs):
        """
        修改API用例树形结构
        :param request:
        :param api_test_task_id: api任务id
        :param args:
        :param kwargs:
        :return:
        """

        if api_test_task_id == "":
            return MyException("任务id不能为空")
        api_test_task = APITestTask.objects.get(id=api_test_task_id)
        api_case_list_data = json.loads(api_test_task.cases)
        api_task_data = {
            "api_test_task_name": api_test_task.api_test_task_name,
            "describe": api_test_task.describe
        }
        api_projects = APIProject.objects.all()
        data_list = []
        for api_project in api_projects:
            api_project_dict = {
                "api_project_name": api_project.api_project_name,
                "isParent": True
            }
            ui_case_list = []
            api_test_cases = ApiBusinessTest.objects.filter(api_project_id=api_project.id)
            for api_test_case in api_test_cases:
                if api_test_case.id in api_case_list_data:
                    ui_case_dict = {
                        "api_test_case_name": api_test_case.ui_test_case_name,
                        "api_test_case_id": api_test_case.id,
                        "isParent": False,
                        "checked": True,
                    }
                else:
                    ui_case_dict = {
                        "api_test_case_name": api_test_case.ui_test_case_name,
                        "api_test_case_id": api_test_case.id,
                        "isParent": False,
                        "checked": False,
                    }
                ui_case_list.append(ui_case_dict)

            api_project_dict["children"] = ui_case_list
            data_list.append(api_project_dict)
        api_task_data["cases"] = data_list
        return response_success(api_task_data)


class CheckApiResultList(View):

    def get(self, request, api_test_task_id, *args, **kwargs):
        """
        查看API测试报告列表
        :param request:
        :param api_test_task_id:
        :param args:
        :param kwargs:
        :return:
        """
        if api_test_task_id == "":
            return response_failed({"status": 10102, "message": "api_test_task_id不能为空"})
        r = APITestResult.objects.filter(api_task_id=api_test_task_id)
        data = []
        for i in r:
            result = {
                "id": i.id,
                "api_test_result_name": i.api_test_result_name,
                "create_time": i.create_time,
                "api_error_total_number": i.api_error_total_number,
                "api_successful_total_number": i.api_successful_total_number,
                "api_total_number": i.api_total_number

            }
            data.append(result)
        return response_success({'status': 10102, 'data': data})

    def get(self, request, api_test_task_id, *args, **kwargs):
        """
        查看API测试报告列表
        :param request:
        :param api_test_task_id:
        :param args:
        :param kwargs:
        :return:
        """
        if api_test_task_id == "":
            return response_failed({"status": 10102, "message": "api_test_task_id不能为空"})
        r = APITestResult.objects.filter(api_task_id=api_test_task_id)
        data = []
        for i in r:
            result = {
                "id": i.id,
                "api_test_result_name": i.api_test_result_name,
                "create_time": i.create_time,
                "api_error_total_number": i.api_error_total_number,
                "api_successful_total_number": i.api_successful_total_number,
                "api_total_number": i.api_total_number

            }
            data.append(result)
        return response_success({'status': 10102, 'data': data})


class CheckApiResult(View):
    def get(self, request, api_test_result_id, size_page, page, *args, **kwargs):
        """
        查看任务--测试报告列表--测试结果列表
        :param size_page: 展示条数
        :param page: 页数
        :param request:
        :param api_test_result_id:
        :param args:
        :param kwargs:
        :return:
        """
        if api_test_result_id == "":
            return response_failed({"status": 10102, "message": "api_test_task_id不能为空"})
        r = APITestResultAssociated.objects.filter(api_result_id=api_test_result_id)

        data = []
        for i in r:
            result = {
                "id": i.id,
                "api_test_case_name": i.api_test_case_name,
                "api_task_name": i.api_task.api_test_task_name,
                "api_business_test_name": i.api_business_test_name,
                "api_error": i.api_error,
                "api_successful": i.api_successful,
                "abnormal": i.abnormal,
                "json_extract_variable_conversion": i.json_extract_variable_conversion,
                "api_assertion_results": i.api_assertion_results,
                "api_request_results": i.api_request_results,
                "api_result_id": i.api_result_id,
                "api_task_id": i.api_task_id,
                "create_time": i.create_time
            }
            data.append(result)

        p = Paginator(data, size_page)
        page1 = p.page(page)
        current_page = page1.object_list
        api_result = APITestResult.objects.get(id=api_test_result_id)

        case_result_total = [int(api_result.api_successful_total_number), int(api_result.api_error_total_number)]

        return response_success({'status': 10102, 'data': current_page, "case_result_total": case_result_total})

    def post(self, request, api_test_case_result_id, *args, **kwargs):
        """
        查看任务--测试报告列表--测试结果列表--单独测试用例报告
        :param request:
        :param api_test_case_result_id:API测试结果关联表的ID
        :param args:
        :param kwargs:
        :return:
        """
        if api_test_case_result_id == "":
            return response_failed({"status": 10102, "message": "api_test_case_result_id不能为空"})
        r = APITestResultAssociated.objects.filter(id=api_test_case_result_id)
        data = []
        for i in r:
            result = {
                "id": i.id,
                "api_test_case_name": i.api_test_case_name,
                "api_task_name": i.api_task.api_test_task_name,
                "api_business_test_name": i.api_business_test_name,
                "api_error": i.api_error,
                "api_successful": i.api_successful,
                "abnormal": i.abnormal,
                "json_extract_variable_conversion": i.json_extract_variable_conversion,
                "api_assertion_results": i.api_assertion_results,
                "api_request_results": i.api_request_results,
                "api_result_id": i.api_result_id,
                "api_task_id": i.api_task_id,
                "create_time": i.create_time,
                "api_variable_results": i.api_variable_results,
                "api_header": i.api_header,
                "api_url": i.api_url,
                "api_body": i.api_body
            }



            data.append(result)
        return response_success({'status': 10102, 'data': data})

    def delete(self, request, api_test_result_id, *args, **kwargs):
        """
        查看任务--测试报告列表--删除测试报告
        :param request:
        :param api_test_result_id:API测试结果关联表的ID
        :param args:
        :param kwargs:
        :return:
        """
        if api_test_result_id == "":
            return response_failed({"status": 10102, "message": "api_test_result_id不能为空"})
        APITestResult.objects.get(id=api_test_result_id).delete()

        return response_success("删除测试报告成功")


class CheckApiResultErrorList(View):
    def get(self, request, api_test_result_id, size_page, page, *args, **kwargs):
        """
        查看任务--测试报告列表--测试结果列表
        :param size_page: 展示条数
        :param page: 页数
        :param request:
        :param api_test_result_id:
        :param args:
        :param kwargs:
        :return:
        """
        print(api_test_result_id)
        if api_test_result_id == "":
            return response_failed({"status": 10102, "message": "api_test_task_id不能为空"})
        r = APITestResultAssociated.objects.filter(api_result_id=api_test_result_id, api_error=1)

        data = []
        for i in r:
            result = {
                "id": i.id,
                "api_test_case_name": i.api_test_case_name,
                "api_task_name": i.api_task.api_test_task_name,
                "api_business_test_name": i.api_business_test_name,
                "api_error": i.api_error,
                "api_successful": i.api_successful,
                "abnormal": i.abnormal,
                "json_extract_variable_conversion": i.json_extract_variable_conversion,
                "api_assertion_results": i.api_assertion_results,
                "api_request_results": i.api_request_results,
                "api_result_id": i.api_result_id,
                "api_task_id": i.api_task_id,
                "create_time": i.create_time
            }
            data.append(result)

        p = Paginator(data, size_page)
        page1 = p.page(page)
        current_page = page1.object_list
        api_result = APITestResult.objects.get(id=api_test_result_id)

        case_result_total = [int(api_result.api_successful_total_number), int(api_result.api_error_total_number)]
        print(case_result_total)

        return response_success({'status': 10102, 'data': current_page, "case_result_total": case_result_total})


class PerformApiTask(View):

    def post(self, request, api_test_task_id, *args, **kwargs):
        """
        执行当前API任务
        :param request:
        :param api_test_task_id:
        :param args:
        :param kwargs:
        :return:
        """

        if api_test_task_id == "":
            return response_failed({"status": 10200, "message": "api_test_task_id is null"})

        # 1、在执行线程之前，判断当前有没有任务在执行？
        tasks = APITestTask.objects.all()
        for t in tasks:
            if t.status == 1:
                return response_failed({"status": 10200, "message": "当前有任务正在执行！"})

        # 2. 修改任务的状态为：1-执行中
        task = APITestTask.objects.get(id=api_test_task_id)
        task.status = 1
        task.save()

        # 通过多线程运行测试任务
        TaskThread(api_test_task_id).run()
        return response_success({"status": 10200, "message": "任务开始执行！"})

