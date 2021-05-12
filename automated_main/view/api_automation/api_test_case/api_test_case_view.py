# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 10:50
# @Author  : wangyinghao
# @FileName: api_test_case_view.py
# @Software: PyCharm
from django.views.generic import View
import json
import re
import requests
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.exception.my_exception import MyException
from automated_main.models.api_automation.api_test_case import ApiTestCase
from automated_main.form.api_test_case import ApiTestCaseForm
from automated_main.models.api_automation.api_environment import APIEnvironment



class ApiTestCaseView(View):

    def delete(self, request, api_test_case_id, *args, **kwargs):
        """
         代表删除API测试用例
        :param request:
        :param api_test_case_id:
        :param args:
        :param kwargs:
        :return:
        """

        ApiTestCase.objects.get(id=api_test_case_id).delete()
        return response_success("删除API测试用例成功")

    def put(self, request, *args, **kwargs):
        """
        创建API测试用例
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
        form = ApiTestCaseForm(data)
        if form.is_valid():
            ApiTestCase.objects.create(**form.cleaned_data)
            return response_success("创建API测试用例成功")
        else:
            raise MyException()

    def post(self, request, api_test_case_id, *args, **kwargs):
        """
        编辑API测试用例
        :param request:
        :param args:
        :param api_test_case_id:
        :param kwargs:
        :return:
        """

        api_test_case = ApiTestCase.objects.filter(id=api_test_case_id).first()
        if api_test_case is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()

        data = json.loads(body)
        form = ApiTestCaseForm(data)
        if form.is_valid():
            ApiTestCase.objects.filter(id=api_test_case_id).update(**form.cleaned_data)
            return response_success("修改API测试用例成功")
        else:
            raise MyException()

    def get(self, request, api_test_case_id, *args, **kwargs):
        """
        获取单独API测试用例
        :param request:
        :param args:
        :param api_test_case_id:
        :param kwargs:
        :return:
        """

        api_test_case = ApiTestCase.objects.filter(id=api_test_case_id).first()
        if api_test_case is None:
            return response_success()
        else:
            return response_success(model_to_dict(api_test_case))


class ApiTestCaseDeBugView(View):

    def post(self, request, *args, **kwargs):
        """
        API测试用例调试
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body

        if not body:
            return response_success()

        data = json.loads(body)
        api_environment = APIEnvironment.objects.get(id=data['api_environment_id'])

        # 请求地址
        api_url = api_environment.api_title + data['api_url']

        if "${" in api_url and "}" in api_url:
            key = re.findall(r"\${(.+?)}", api_url)
            for a in range(len(key)):
                key1 = "${" + key[a] + "}"
                value_variable = ApiTestCase.objects.filter(api_key_variable=key1)
                variable = value_variable[0].api_variable_results
                api_url = api_url.replace(key1, variable)

        if "${" in data['api_headers'] and "}" in data['api_headers']:
            key = re.findall(r"\${(.+?)}", data['api_headers'])
            for b in range(len(key)):
                key1 = "${" + key[b] + "}"
                value_variable = ApiTestCase.objects.filter(api_key_variable=key1)
                variable = value_variable[0].api_variable_results
                data['api_headers'] = data['api_headers'].replace(key1, variable)

        json_header = data['api_headers'].replace("\'", "\"")
        if data['api_headers'] == '':
            header = data['api_headers']
        else:
            try:
                header = json.loads(json_header)
            except json.decoder.JSONDecodeError:
                return response_failed("30000", "header类型错误")

        if "${" in data['api_parameter_body'] and "}" in data['api_parameter_body']:
            key = re.findall(r"\${(.+?)}", data['api_parameter_body'])
            for b in range(len(key)):
                key1 = "${" + key[b] + "}"
                value_variable = ApiTestCase.objects.filter(api_key_variable=key1)
                variable = value_variable[0].api_variable_results
                data['api_parameter_body'] = data['api_parameter_body'].replace(key1, variable)

        json_par = data['api_parameter_body'].replace("\'", "\"")

        if data['api_parameter_body'] == '':
            payload = data['api_parameter_body']
        else:
            try:
                payload = json.loads(json_par)
            except json.decoder.JSONDecodeError:
                return response_failed("30000", "参数类型错误")

        """
        data['api_method']类型：
        1:get
        2:post
        3:put
        4:delete
        
        data['api_parameter_types']类型：
        1:form-data
        2:JSON
        3.x-www-form-urlencoded
        4.none
        """
        # 请求方法
        api_method = str(data['api_method'])

        # 参数类型
        api_parameter_types = str(data['api_parameter_types'])

        # Get
        if api_method == "1":
            if data['api_headers'] == "":
                r = requests.get(api_url, params=payload)
                print(r.json())
            else:
                r = requests.get(api_url, params=payload, headers=header)
                print(r.json())

        # Post
        if api_method == "2":
            if api_parameter_types == "1":
                if data['api_headers'] == "":
                    r = requests.post(api_url, data=payload)
                    print(r.text)
                else:
                    r = requests.post(api_url, data=payload, headers=header)
                    print(r.text)
            if api_parameter_types == "2":
                if data['api_headers'] == "":
                    r = requests.post(api_url, json=payload)
                    print(r.text)
                else:
                    r = requests.post(api_url, json=payload, headers=header)
                    print(r.text)
            if api_parameter_types == "3":
                if data['api_headers'] == "":
                    r = requests.post(api_url, data=payload)
                    print(r.text)
                else:
                    r = requests.post(api_url, data=payload, headers=header)
                    print(r.text)

        # Put
        if api_method == "3":
            if api_parameter_types == "1":
                if data['api_headers'] == "":
                    r = requests.put(api_url, data=payload)
                    print(r.text)
                else:
                    r = requests.put(api_url, data=payload, headers=header)
                    print(r.text)
            if api_parameter_types == "2":
                if data['api_headers'] == "":
                    r = requests.put(api_url, json=payload)
                    print(r.text)
                else:
                    r = requests.put(api_url, json=payload, headers=header)
                    print(r.text)

        # Delete
        if api_method == "4":
            if api_parameter_types == "1":
                if data['api_headers'] == "":
                    r = requests.delete(api_url, data=payload)
                    print(r.text)
                else:
                    r = requests.delete(api_url, data=payload, headers=header)
                    print(r.text)
            if api_parameter_types == "2":
                if data['api_headers'] == "":
                    r = requests.delete(api_url, json=payload)
                    print(r.text)
                else:
                    r = requests.delete(api_url, json=payload, headers=header)
                    print(r.text)

        # 断言
        if data['api_assert_type'] == '':
            result = "断言内容为空"

        elif data['api_assert_type'] == 1:
            try:
                assert (data['api_assert_text'] in r.text)
                result = "断言成功"
            except Exception as e:
                result = "断言失败" + str(e)
                print(str(e))
                pass

        elif data['api_assert_type'] == 2:
            if data['api_assert_text'] != r.text():
                result = "断言失败"
            else:
                result = "断言成功"

        # 提取变量
        api_result = json.loads(r.text)
        if data['api_value_variable'] == "":
            api_variable_results = "无参数提取"

        else:
            v_text = data['api_value_variable'].split(".")
            print('这是提取',v_text)

            try:
                for a in v_text:
                    if "[" in a and "]" in a:
                        variable_1 = a.split('[')[0]
                        variable_2 = a.split('[')[1].split(']')[0]
                        api_result = api_result[variable_1][int(variable_2)]
                        print('ssssssssss',api_result)
                    else:
                        api_result = api_result[a]
                        print('xxxxxxxxx',api_result)

                api_variable_results = str(api_result)
            except Exception as e:
                print(e)
                api_variable_results = "参数提取失败：" + str(e)

        return response_success({'api_url': r.url,
                                 'api_header': str(r.headers),
                                 'api_body': str(payload),
                                 'api_code': str(r.status_code),
                                 'api_assert': str(result),
                                 'response_message': r.json(),
                                 'response_time': str(r.elapsed.total_seconds()),
                                 'api_variable_results': api_variable_results})
