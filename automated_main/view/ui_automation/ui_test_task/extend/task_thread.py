import os
import json
import threading
from time import sleep
from automated_main.models.ui_automation.ui_test_case import UITestCase, UITestCaseAssociated
from automated_main.models.ui_automation.ui_test_task import UITestTask
from automated_main.models.ui_automation.ui_test_task import UITestResult
from automated_main.view.ui_automation.ui_test_task.extend.setting import TASK_RESULTS
from AutomatedTestPlatform import settings
import re
from xml.dom.minidom import parse
from xml.dom import minidom
from bs4 import BeautifulSoup


BASE_PATH = settings.BASE_DIR.replace("\\", "/")
EXTEND_DIR = BASE_PATH + "/automated_main/view/ui_automation/ui_test_task/extend/"
print("运行文件的目录--->", EXTEND_DIR)


class TaskThread:

    def __init__(self, task_id):
        self.tid = task_id

    def run_cases(self):
        print("运行某一个任务下面的所有测试用例")

        ui_task = UITestTask.objects.get(id=self.tid)
        # 1. 拿到任务对应用例的列表
        ui_case_list = json.loads(ui_task.cases)
        print("拿到任务对应用例的列表", ui_task.cases)

        # 2. 将用例数据写到 json文件
        test_data = {}
        for cid in ui_case_list:
            print(cid)
            ui_test_case = UITestCase.objects.get(id=cid)
            ui_associated = UITestCaseAssociated.objects.filter(cid_id=cid).order_by("case_steps")
            print(ui_test_case.ui_project_id)

            data_list = []
            for ui_associateds in ui_associated:

                ui_associated_dict = {
                    "ui_elements_id": ui_associateds.ui_page_elements_id,
                    "element_operation": ui_associateds.element_operation,
                    "element_input": ui_associateds.element_input,
                    "waiting_time": ui_associateds.waiting_time,
                    "x_coordinates": ui_associateds.x_coordinates,
                    "y_coordinates": ui_associateds.y_coordinates,

                }
                data_list.append(ui_associated_dict)
            print(data_list)
            test_data[ui_test_case.id] = data_list
        case_data = json.dumps(test_data, sort_keys=True)
        print("将用例数据写到 json文件", case_data)
        print("xxxxxxxxxxxxx", EXTEND_DIR)

        with(open(EXTEND_DIR + "test_data_list.json", "w")) as f:
            f.write(case_data)

        # 3.执行运行测试用例的文件， 它会生成 result.html 文件
        run_cmd = "python3  " + EXTEND_DIR + "run_task.py"
        print("运行的命令", run_cmd)
        os.system(run_cmd)
        sleep(3)

        # 4. 读取result.html文件，把这里面的结果放到表里面。
        print("----------------->保存测试结果")
        self.save_result()
        print("----------------->保存完成")
        # 5. 修改任务的状态，执行完成
        task = UITestTask.objects.get(id=self.tid)
        task.status = 2
        task.save()

    def save_result(self):
        """保存测试结果"""
        print("保存测试结果")
        # f = open(TASK_RESULTS, 'r', encoding='GBK')
        f = open(TASK_RESULTS, 'r', encoding='UTF-8')
        html_results = f.read()
        f.close()

        soup = BeautifulSoup(open(TASK_RESULTS, encoding='UTF-8'), 'html.parser')
        failures = soup.select('#show_detail_line > a.btn.btn-warning')
        for a in failures:
            failures = a.string
        failure = failures.strip(failures[0] + failures[1] + failures[2] + failures[3] + failures[5] + failures[6])
        print("类型", type(failure))
        print(failure)

        errors = soup.select('#show_detail_line > a.btn.btn-danger')
        for a in errors:
            errors = a.string
        error = errors.strip(errors[0] + errors[1] + errors[2] + errors[3] + errors[5] + errors[6])
        print(error)

        successful = soup.select('#show_detail_line > a.btn.btn-success')
        for a in successful:
            successful = a.string
        successfuls = successful.strip(successful[0] + successful[1] + successful[2] + successful[3] + successful[5] + successful[6])
        print(successfuls)

        tests = soup.select('#show_detail_line > a.btn.btn-info')
        for a in tests:
            tests = a.string

        test = tests.strip(tests[0] + tests[1] + tests[2] + tests[3] + tests[5] + tests[6])
        print(test)

        time = soup.select('#div_base > div.heading > p:nth-child(4)')
        for a in time:
            time = a.get_text()

        time_consuming = time.strip(time[0] + time[1] + time[2] + time[3] + time[4] + time[5] + time[6] + time[7] + time[-0])
        print(time_consuming)

        name = soup.select('#div_base > div.heading > p.description')
        for a in name:
            name = a.get_text()
        print(name)

        UITestResult.objects.create(
            ui_task_id=self.tid,
            ui_test_result_name=name,
            error=int(error),
            failure=int(failure),
            skipped=int(0),
            tests=int(test),
            run_time=time_consuming,
            result=html_results,
            successful=int(successfuls),

        )

    def run_tasks(self):
        print("创建线程任务...")
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
    print("开始")
    # run()  # 丢给线程去运行任务
    TaskThread(1).run()
    print("结束")
