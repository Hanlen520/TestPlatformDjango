import os
import json
import threading
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutomatedTestPlatform.settings")
django.setup()
from time import sleep
from automated_main.models.api_automation.api_business_test import ApiBusinessTest, ApiBusinessTestAssociated
from automated_main.models.api_automation.api_test_task import APITestTask
from automated_main.models.api_automation.api_test_task import APITestResult
from automated_main.models.api_automation.api_test_case import ApiTestCase, ApiParameterExtraction
from automated_main.models.api_automation.api_test_task import APITestResultAssociated
from automated_main.view.api_automation.api_test_task.extend.setting import TASK_RESULTS
from AutomatedTestPlatform import settings
import time
import logging
import re
from xml.dom.minidom import parse
from xml.dom import minidom
from bs4 import BeautifulSoup


BASE_PATH = settings.BASE_DIR.replace("\\", "/")
EXTEND_DIR = BASE_PATH + "/automated_main/view/api_automation/api_test_task/extend/"
# EXTEND_DIR = BASE_PATH + "\\automated_main\\view\\api_automation\\api_test_task\\extend\\"
logger = logging.getLogger('django')


class TaskThread:

    def __init__(self, task_id):
        self.tid = task_id

    def run_cases(self):
        logger.info("运行某一个任务下面的所有测试用例")

        api_task = APITestTask.objects.get(id=self.tid)
        # 1. 拿到任务对应用例的列表
        api_case_list = json.loads(api_task.cases)

        logger.info("拿到任务对应用例的列表" + api_task.cases)
        now = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
        api_result = APITestResult.objects.create(
            api_task_id=self.tid,
            api_test_result_name=now
        )

        # 2. 将API用例数据写到 json文件
        test_data = {}
        for cid in api_case_list:
            logger.info(cid)
            api_business_test = ApiBusinessTest.objects.get(id=cid)
            api_associated = ApiBusinessTestAssociated.objects.filter(bid_id=cid)

            data_list = []
            for api_associateds in api_associated:
                api_test_case = ApiTestCase.objects.get(id=api_associateds.api_test_case_id)
                api_parameter_extraction = ApiParameterExtraction.objects.filter(api_test_case_id=api_associateds.api_test_case_id)

                api_parameter_extraction_list = []
                api_associated_dict = {
                    "api_business_test_name": api_business_test.api_business_test_name,
                    "api_result_id": api_result.id,
                    "api_task_id": self.tid,
                    "api_test_case_id": api_associateds.api_test_case_id,
                    "api_test_case_name": api_test_case.api_test_case_name,
                    "api_method": api_test_case.api_method,
                    "api_url": api_test_case.api_environment.api_title + api_test_case.api_url,
                    "api_parameter_types": api_test_case.api_parameter_types,
                    "api_headers": api_test_case.api_headers,
                    "api_parameter_body": api_test_case.api_parameter_body,
                    "api_assert_type": api_test_case.api_assert_type,
                    "api_assert_text": api_test_case.api_assert_text,
                    "api_parameter_extraction": api_parameter_extraction_list,
                    "case_steps": int(api_associateds.case_steps)
                }

                for api_parameter_extractions in api_parameter_extraction:
                    api_parameter_extraction_dict ={
                        "api_value_variable": api_parameter_extractions.api_value_variable,
                        "api_key_variable": api_parameter_extractions.api_key_variable,
                        "api_variable_results": api_parameter_extractions.api_variable_results,

                    }
                    api_parameter_extraction_list.append(api_parameter_extraction_dict)

                data_list.append(api_associated_dict)

            data_list_sorting = sorted(data_list, key=lambda x: x['case_steps'])
            test_data[api_business_test.api_business_test_name] = data_list_sorting
        case_data = json.dumps(test_data, sort_keys=True)
        logger.info("将用例数据写到 json文件" + case_data)

        with(open(EXTEND_DIR + "test_data_list.json", "w")) as f:
            f.write(case_data)

        # 3.执行运行测试用例的文件 本地是python 测试环境是python3
        ENV_PROFILE = os.getenv("ENV")
        if ENV_PROFILE == "SERVER":
            python = 'python3 '
        elif ENV_PROFILE == "1":
            python = 'python '

        run_cmd = python + EXTEND_DIR + "run_task.py"
        logger.info("运行的命令" + run_cmd)
        os.system(run_cmd)
        sleep(10)

        logger.info(api_result.id)
        api_total_number = APITestResultAssociated.objects.filter(api_result_id=api_result.id).count()
        api_error_total_number = APITestResultAssociated.objects.filter(api_result_id=api_result.id, api_error=1).count()
        api_successful_total_number = APITestResultAssociated.objects.filter(api_result_id=api_result.id, api_successful=1).count()
        api_test_result = APITestResult.objects.get(id=api_result.id)
        api_test_result.api_error_total_number = api_error_total_number
        api_test_result.api_successful_total_number = api_successful_total_number
        api_test_result.api_total_number = api_total_number
        api_test_result.save()

        # 4. 修改任务的状态，执行完成
        task = APITestTask.objects.get(id=self.tid)
        task.status = 2
        task.save()

    def run_tasks(self):
        logger.info("创建线程任务...")
        sleep(2)
        threads = []
        t1 = threading.Thread(target=self.run_cases)
        threads.append(t1)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def run(self):
        threads = []
        t = threading.Thread(target=self.run_tasks)
        threads.append(t)

        for t in threads:
            t.start()


if __name__ == '__main__':
    logger.info("开始")
    # run()  # 丢给线程去运行任务
    TaskThread(1).run()
    logger.info("结束")
