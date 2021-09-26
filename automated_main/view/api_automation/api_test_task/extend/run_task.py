# -*- coding: utf-8 -*-
# @Time    : 2020/7/4 16:27
# @Author  : wangyinghao
# @FileName: run_task.py
# @Software: PyCharm
import sys
import json
import os, django
import re
import unittest
from ddt import ddt, file_data, unpack
from os.path import dirname, abspath
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
BASE_PATH = BASE_DIR.replace("\\", "/")
sys.path.append(BASE_PATH)
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.extend(['/home/AutomatedTestPlatform'])
# project_name 项目名称
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutomatedTestPlatform.settings")
django.setup()
from automated_main.models.api_automation.api_test_case import ApiTestCase, ApiParameterExtraction
from automated_main.models.api_automation.api_test_task import APITestResultAssociated
from automated_main.view.api_automation.api_test_task.extend.report.HTMLTestReportCN import HTMLTestRunner
import time
import requests
import logging
logger = logging.getLogger('django')

logger.info("运行测试文件：" + BASE_PATH)

# 定义扩展的目录
EXTEND_DIR = BASE_PATH + "/api_test_task/extend/"
logger.info("地址信息" + EXTEND_DIR)


@ddt
class InterfaceTest(unittest.TestCase):
    def setUp(self):
        pass

    @unpack
    @file_data("test_data_list.json")
    def test_run_cases(self, case_id):

        for case in case_id:
            api_test_case_id = (case['api_test_case_id'])
            api_test_case_name = (case['api_test_case_name'])
            api_url = (case['api_url'])
            api_method = (case['api_method'])
            api_parameter_types = (case['api_parameter_types'])
            api_headers = (case['api_headers'])
            api_parameter_body = (case['api_parameter_body'])
            api_assert_type = (case['api_assert_type'])
            # api_value_variable = (case['api_value_variable'])
            api_parameter_extraction = (case['api_parameter_extraction'])

            api_assert_text = (case['api_assert_text'])
            api_result_id = (case['api_result_id'])
            api_task_id = (case['api_task_id'])
            api_business_test_name = (case['api_business_test_name'])
            api_assertion_results = ""
            json_loads = ""
            api_error = ""
            api_successful = ""
            api_variable_results = ""
            abnormal = ""

            try:
                if "${" in api_url and "}" in api_url:
                    key = re.findall(r"\${(.+?)}", api_url)
                    for a in range(len(key)):
                        key1 = "${" + key[a] + "}"
                        value_variable = ApiParameterExtraction.objects.filter(api_key_variable=key1)
                        variable = value_variable[0].api_variable_results
                        api_url = api_url.replace(key1, variable)

                if api_headers == "{}" or "":
                    header_dict = {}
                else:

                    if "${" in api_headers and "}" in api_headers:
                        key = re.findall(r"\${(.+?)}", api_headers)
                        for b in range(len(key)):
                            key1 = "${" + key[b] + "}"
                            value_variable = ApiParameterExtraction.objects.filter(api_key_variable=key1)
                            variable = value_variable[0].api_variable_results
                            api_headers = api_headers.replace(key1, variable)

                    header = api_headers.replace("\'", "\"")

                    header_dict = json.loads(header)

                if api_parameter_body == "{}" or "":
                    api_parameter_body_dict = {}
                else:
                    if "${" in api_parameter_body and "}" in api_parameter_body:
                        key = re.findall(r"\${(.+?)}", api_parameter_body)
                        for b in range(len(key)):
                            key1 = "${" + key[b] + "}"
                            value_variable = ApiParameterExtraction.objects.filter(api_key_variable=key1)
                            variable = value_variable[0].api_variable_results
                            api_parameter_body = api_parameter_body.replace(key1, variable)

                    api_parameter = api_parameter_body.replace("\'", "\"")
                    api_parameter_body_dict = json.loads(api_parameter)

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
                # 增加接口等待时间
                # time.sleep(2)

                # Get
                if api_method == 1:
                    if api_parameter_types == 1:
                        r = requests.get(api_url, params=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)
                        1
                    if api_parameter_types == 2:
                        r = requests.get(api_url, json=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)
                    if api_parameter_types == 3:
                        r = requests.get(api_url, data=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)

                # Post
                if api_method == 2:
                    if api_parameter_types == 1:
                        r = requests.post(api_url, data=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)
                    if api_parameter_types == 2:
                        r = requests.post(api_url, json=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)
                    if api_parameter_types == 3:
                        r = requests.post(api_url, data=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)

                # Put
                if api_method == 3:
                    if api_parameter_types == 1:
                        r = requests.put(api_url, data=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)
                    if api_parameter_types == 2:
                        r = requests.put(api_url, json=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)
                    if api_parameter_types == 3:
                        r = requests.put(api_url, data=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)

                # Delete
                if api_method == 4:
                    if api_parameter_types == 1:
                        r = requests.delete(api_url, data=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)
                    if api_parameter_types == 2:
                        r = requests.delete(api_url, json=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)
                    if api_parameter_types == 3:
                        r = requests.delete(api_url, data=api_parameter_body_dict, headers=header_dict)
                        logger.info(r.text)

                if api_assert_type == '':
                    api_error = 0
                    api_successful = 1
                    api_assertion_results = "断言成功"

                elif api_assert_type == 1:
                    try:
                        self.assertIn(api_assert_text, r.text)
                        api_error = 0
                        api_successful = 1
                        api_assertion_results = "断言成功"
                    except Exception as e:
                        logger.error("断言失败，用例名称是：" + api_test_case_name + "断言失败：" + str(e))
                        api_assertion_results = "断言失败：" + str(e)
                        api_error = 1
                        api_successful = 0
                        pass

                elif api_assert_type == 2:
                    try:
                        self.assertEqual(api_assert_text, r.text)
                        api_error = 0
                        api_successful = 1
                        api_assertion_results = "断言成功"
                    except Exception as e:
                        logger.error("断言失败，用例名称是：" + api_test_case_name + "断言失败：" + str(e))
                        api_assertion_results = "断言失败：" + str(e)
                        api_error = 1
                        api_successful = 0
                        pass
                elif api_assert_type == 3:
                    try:
                        self.assertEqual(api_assert_text, r.status_code)
                        api_error = 0
                        api_successful = 1
                        api_assertion_results = "断言成功"
                    except Exception as e:
                        logger.error("断言失败，用例名称是：" + api_test_case_name + "断言失败：" + str(e))
                        api_assertion_results = "断言失败：" + str(e)
                        api_error = 1
                        api_successful = 0
                        pass

                if ApiParameterExtraction.objects.filter(api_test_case_id=api_test_case_id).count() > 0:
                    ApiParameterExtraction.objects.filter(api_test_case_id=api_test_case_id).delete()

                    for api_parameter_extractions in api_parameter_extraction:

                        if api_parameter_extractions['api_value_variable'] == "":
                            pass
                        else:
                            v_text = api_parameter_extractions['api_value_variable'].split(".")
                            # 提取变量
                            try:
                                api_result = json.loads(r.text)
                            except Exception as e:
                                json_loads = "提取变量json.loads(r.text) 失败：" + str(e)
                                logger.error("提取变量json.loads(r.text) 失败：" + str(e))
                                pass
                            try:
                                for a in v_text:
                                    if "[" in a and "]" in a:
                                        variable_1 = a.split('[')[0]
                                        variable_2 = a.split('[')[1].split(']')[0]
                                        api_result = api_result[variable_1][int(variable_2)]
                                    else:
                                        api_result = api_result[a]

                                api_variable_results = str(api_result)
                            except Exception as e:
                                api_variable_results = "参数提取失败：" + str(e)
                                logger.error(api_variable_results)
                                pass


                            logger.info("自定义变量表中有该case_id")

                            ApiParameterExtraction.objects.create(api_test_case_id=api_test_case_id,
                                                                  api_variable_results=api_variable_results,
                                                                  api_value_variable=api_parameter_extractions[
                                                                      'api_value_variable'],
                                                                  api_key_variable=api_parameter_extractions[
                                                                      'api_key_variable'])
                else:
                    logger.info("自定义变量表中 无 该 case_id")

                    for api_parameter_extractions in api_parameter_extraction:

                        if api_parameter_extractions['api_key_variable'] == "":
                            pass
                        else:
                            v_text = api_parameter_extractions['api_value_variable'].split(".")
                            # 提取变量
                            try:
                                api_result = json.loads(r.text)
                            except Exception as e:
                                json_loads = "提取变量json.loads(r.text) 失败：" + str(e)
                                logger.error("提取变量json.loads(r.text) 失败：" + str(e))
                                pass
                            try:
                                for a in v_text:
                                    if "[" in a and "]" in a:
                                        variable_1 = a.split('[')[0]
                                        variable_2 = a.split('[')[1].split(']')[0]
                                        api_result = api_result[variable_1][int(variable_2)]
                                    else:
                                        api_result = api_result[a]

                                api_variable_results = str(api_result)
                            except Exception as e:
                                api_variable_results = "参数提取失败：" + str(e)
                                logger.error(api_variable_results)
                                pass

                            if ApiParameterExtraction.objects.filter(api_key_variable=api_parameter_extractions['api_key_variable']).count() > 0:
                                api_parameter_extraction_list = (str(api_parameter_extractions['api_key_variable']) + "变量名称重复,请重新填写")
                            else:
                                ApiParameterExtraction.objects.create(api_test_case_id=api_test_case_id,
                                                                      api_variable_results=api_parameter_extractions['api_variable_results'],
                                                                      api_value_variable=api_variable_results,
                                                                      api_key_variable=api_parameter_extractions['api_key_variable'])

                api_parameter_extraction = ApiParameterExtraction.objects.filter(api_test_case_id=api_test_case_id)

                api_parameter_extraction_list = []
                if api_parameter_extraction.count() > 0:
                    for api_parameter_extractions in api_parameter_extraction:
                        api_parameter_extraction_dict = {
                            "api_key_variable": api_parameter_extractions.api_key_variable,
                            "api_variable_results": api_parameter_extractions.api_variable_results

                        }
                        api_parameter_extraction_list.append(api_parameter_extraction_dict)
                print(api_parameter_extraction_list)

                APITestResultAssociated.objects.create(api_test_case_name=api_test_case_name, api_error=api_error,
                                                       api_successful=api_successful, abnormal=abnormal,
                                                       json_extract_variable_conversion=json_loads,
                                                       api_assertion_results=api_assertion_results,
                                                       api_variable_results=str(api_parameter_extraction_list),
                                                       api_request_results=r.json(),
                                                       api_result_id=api_result_id,
                                                       api_task_id=api_task_id,
                                                       api_business_test_name=api_business_test_name,
                                                       api_url=api_url,
                                                       api_body=api_parameter_body_dict,
                                                       api_header=header_dict
                                                       )
            except Exception as e:
                abnormal = str(e)
                if api_assertion_results == "断言成功":
                    api_error = 0
                    api_successful = 1
                    APITestResultAssociated.objects.create(api_test_case_name=api_test_case_name, api_error=api_error,
                                                           api_successful=api_successful, abnormal=abnormal,
                                                           json_extract_variable_conversion=json_loads,
                                                           api_assertion_results=api_assertion_results,
                                                           api_variable_results=str(api_parameter_extraction_list),
                                                           api_request_results=r.text,
                                                           api_result_id=api_result_id,
                                                           api_task_id=api_task_id,
                                                           api_business_test_name=api_business_test_name,
                                                           api_url=api_url,
                                                           api_header=header_dict,
                                                           api_body=api_parameter_body_dict,
                                                           )
                else:
                    api_error = 0
                    api_successful = 1
                    APITestResultAssociated.objects.create(api_test_case_name=api_test_case_name, api_error=api_error,
                                                           api_successful=api_successful, abnormal=abnormal,
                                                           json_extract_variable_conversion=json_loads,
                                                           api_assertion_results=api_assertion_results,
                                                           api_variable_results=str(api_parameter_extraction_list),
                                                           api_request_results=r.json(),
                                                           api_result_id=api_result_id,
                                                           api_task_id=api_task_id,
                                                           api_business_test_name=api_business_test_name,
                                                           api_url=api_url,
                                                           api_header=header_dict,
                                                           api_body=api_parameter_body_dict,
                                                           )
            continue

    def tearDown(self):
        pass


def run_cases():
    now = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
    testunit = unittest.TestSuite()
    testunit.addTest(unittest.TestLoader().loadTestsFromTestCase(InterfaceTest))
    filename = EXTEND_DIR + 'results.html'

    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp,
                                title='API测试报告',
                                description=now,
                                verbosity=2)
        runner.run(testunit)


if __name__ == '__main__':

    unittest.main(verbosity=2)





