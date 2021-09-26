import os
import json
import threading
from time import sleep
from automated_main.models.ui_automation.ui_test_case import UITestCase, UITestCaseAssociated
from automated_main.models.ui_automation.ui_test_task import UITestTask
from automated_main.models.ui_automation.ui_test_task import UITestResult, UITestResultAssociated
from automated_main.view.ui_automation.ui_test_task.extend.setting import TASK_RESULTS
from AutomatedTestPlatform import settings
import re
import random
import time
from xml.dom.minidom import parse
from xml.dom import minidom
from bs4 import BeautifulSoup
import logging
logger = logging.getLogger('django')


BASE_PATH = settings.BASE_DIR.replace("\\", "/")
EXTEND_DIR = BASE_PATH + "/automated_main/view/ui_automation/ui_test_task/extend/"
logger.info("运行文件的目录--->" + EXTEND_DIR)


class TaskThread:

    def __init__(self, task_id):
        self.tid = task_id

    def run_cases(self):
        logger.info("运行某一个任务下面的所有测试用例")

        ui_task = UITestTask.objects.get(id=self.tid)
        # 1. 拿到任务对应用例的列表
        ui_case_list = json.loads(ui_task.cases)
        logger.info("拿到任务对应用例的列表" + ui_task.cases)

        fn = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        path = os.path.join(settings.WEB_ROOT, fn)
        filename = path + '.py'
        logger.info("这是保存地址")
        logger.info(filename)

        now = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
        ui_result = UITestResult.objects.create(
            ui_task_id=self.tid,
            ui_test_result_name=now,
            ui_test_script=str(fn + '.py')
        )

        # 2. 将用例数据写到 json文件
        test_data = {}
        for cid in ui_case_list:
            logger.info(cid)
            ui_test_case = UITestCase.objects.get(id=cid)
            ui_associated = UITestCaseAssociated.objects.filter(cid_id=cid)
            logger.info(ui_test_case.ui_project_id)

            data_list = []
            for ui_associateds in ui_associated:

                ui_associated_dict = {
                    "ui_result_id": ui_result.id,
                    "ui_elements_id": ui_associateds.ui_page_elements_id,
                    "element_operation": ui_associateds.element_operation,
                    "element_input": ui_associateds.element_input,
                    "waiting_time": ui_associateds.waiting_time,
                    "x_coordinates": ui_associateds.x_coordinates,
                    "y_coordinates": ui_associateds.y_coordinates,
                    "ui_test_case_name": ui_test_case.ui_test_case_name,
                    "ui_task_id": ui_task.id,
                    "case_steps": int(ui_associateds.case_steps),
                    "ui_test_script": filename

                }
                data_list.append(ui_associated_dict)
            data_list_sorting = sorted(data_list, key=lambda x: x['case_steps'])

            test_data[ui_test_case.ui_test_case_name] = data_list_sorting
        case_data = json.dumps(test_data, sort_keys=True)

        with(open(EXTEND_DIR + "test_data_list.json", "w")) as f:
            f.write(case_data)

        # 3.执行运行测试用例的文件， 它会生成 result.html 文件
        ENV_PROFILE = os.getenv("ENV")
        if ENV_PROFILE == "SERVER":
            python = 'python3 '
        elif ENV_PROFILE == "1":
            python = 'python '

        run_cmd = python + EXTEND_DIR + "run_task.py"
        logger.info("运行的命令" + run_cmd)
        os.system(run_cmd)
        sleep(10)

        logger.info(ui_result.id)
        ui_case_number = ui_task.cases.split(",")
        ui_total_number = len(ui_case_number)

        ui_error_total_number = UITestResultAssociated.objects.filter(ui_result_id=ui_result.id, ui_error=1).count()
        ui_successful_total_number = ui_total_number - ui_error_total_number

        ui_test_result = UITestResult.objects.get(id=ui_result.id)
        ui_test_result.ui_error_total_number = ui_error_total_number
        ui_test_result.ui_successful_total_number = ui_successful_total_number
        ui_test_result.ui_total_number = ui_total_number
        ui_test_result.save()

        # 4. 修改任务的状态，执行完成
        task = UITestTask.objects.get(id=self.tid)
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
