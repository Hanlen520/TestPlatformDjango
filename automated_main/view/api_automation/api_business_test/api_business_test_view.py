# -*- coding: utf-8 -*-
# @Time    : 2021/4/14 18:59
# @Author  : wangyinghao
# @FileName: api_business_test_view.py
# @Software: PyCharm
from django.views.generic import View
import json
import time
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.exception.my_exception import MyException
from automated_main.models.api_automation.api_project import APIProject
from automated_main.models.api_automation.api_module import APIModule
from automated_main.models.api_automation.api_test_case import ApiTestCase
from automated_main.models.api_automation.api_business_test import ApiBusinessTest, ApiBusinessTestAssociated
from automated_main.form.api_business_test import ApiBusinessTestForm


class GetApiBusinessTestSelectData(View):

    def get(self, request, api_project_id, *args, **kwargs):
        """
        获取api项目---模块---测试用例
        :param request:
        :param api_project_id: Api项目id
        :param args:
        :param kwargs:
        :return:
        """
        api_projects = APIProject.objects.filter(id=api_project_id)
        print(api_projects)
        data_list = []
        for api_project in api_projects:
            project_dict = {
                "project_id": api_project.id,
                "api_project_name": api_project.api_project_name
            }

            api_modules = APIModule.objects.filter(api_project_id=api_project.id)
            api_module_list = []
            for api_module in api_modules:
                api_test_cases = ApiTestCase.objects.filter(api_module_id=api_module.id)
                api_test_case_list = []
                for api_test_case in api_test_cases:
                    api_test_case_list.append({
                        "api_test_case_id": api_test_case.id,
                        "api_test_case_name": api_test_case.api_test_case_name,

                    })

                print(api_test_case_list)

                api_module_list.append({
                    "api_module_id": api_module.id,
                    "api_module_name": api_module.api_module_name,
                    "api_test_case_list": api_test_case_list,
                })

            project_dict["module_list"] = api_module_list

            data_list.append(project_dict)
            print(data_list)

        return response_success(data_list)


class ApiBusinessTestView(View):

    def delete(self, request, api_business_test_id, *args, **kwargs):
        """
        代表删除API业务测试
        :param request:
        :param api_business_test_id: 业务测试id
        :param args:
        :param kwargs:
        :return:
        """
        ApiBusinessTest.objects.get(id=api_business_test_id).delete()
        return response_success("删除API业务测试成功")

    def get(self, request, api_business_test_id, *args, **kwargs):
        """
        获取单独API业务测试
        :param request:
        :param api_business_test_id: 业务测试ID
        :param args:
        :param kwargs:
        :return:
        """

        api_business_test = ApiBusinessTest.objects.get(id=api_business_test_id)
        api_business_test_associated = ApiBusinessTestAssociated.objects.filter(bid_id=api_business_test_id).order_by("case_steps")

        if api_business_test is None:
            return response_success()
        else:
            api_business_test_data_list = []
            for api_business_test_associateds in api_business_test_associated:
                api_business_test_dict = {
                    "api_module_id": api_business_test_associateds.api_module_id,
                    "api_test_case_id": api_business_test_associateds.api_test_case_id,
                    "steps": api_business_test_associateds.case_steps,
                }
                api_business_test_data_list.append(api_business_test_dict)

            return response_success({"api_business_test_name": api_business_test.api_business_test_name,
                                     "api_project_id": api_business_test.api_project_id,
                                     "api_business_test_data": api_business_test_data_list})

    def post(self, request, api_business_test_id, *args, **kwargs):
        """
        编辑API业务测试
        :param request:
        :param api_business_test_id:
        :param args:
        :param kwargs:
        :return:
        """
        api_business_test = ApiBusinessTest.objects.get(id=api_business_test_id)
        if api_business_test is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)
        form = ApiBusinessTestForm(data)

        api_business_test.api_business_test_name = data['api_business_test_name']
        api_business_test.api_project.id = data['api_project_id']
        api_business_test.id = data['api_business_test_id']
        api_business_test.save()
        ApiBusinessTestAssociated.objects.filter(bid_id=api_business_test_id).delete()

        if form.is_valid():
            for i in data["api_business_test_data"]:
                api_module_id = (i['api_module_id'])
                api_test_case_id = (i['api_test_case_id'])
                case_steps = (i['steps'])

                ApiBusinessTestAssociated.objects.create(bid_id=api_business_test_id, api_module_id=api_module_id,
                                                         api_test_case_id=api_test_case_id, case_steps=case_steps)
            return response_success("编辑API业务测试")
        else:
            raise MyException()

    def put(self, request, *args, **kwargs):
        """
        创建API业务测试
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
        form = ApiBusinessTestForm(data)
        if form.is_valid():
            api_business_test = ApiBusinessTest.objects.create(**form.cleaned_data)
            api_business_test_id = api_business_test.id

            for i in data["api_business_test_data"]:
                print(i)
                api_module_id = (i['api_module_id'])
                api_test_case_id = (i['api_test_case_id'])
                case_steps = (i['steps'])
                ApiBusinessTestAssociated.objects.create(bid_id=api_business_test_id, api_module_id=api_module_id,
                                                         api_test_case_id=api_test_case_id, case_steps=case_steps)

            return response_success("创建API业务测试用例成功")
        else:
            raise MyException()
