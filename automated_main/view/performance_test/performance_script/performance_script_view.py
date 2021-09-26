# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/27 17:45
@Auth ： WangYingHao
@File ：performance_script_view.py
@IDE ：PyCharm

"""
import json
import os
import random
import time
import arrow
from django.views.generic import View
from AutomatedTestPlatform import settings
from automated_main.exception.my_exception import MyException
from automated_main.form.performance_script import PerformanceScriptForm
from automated_main.models.performance_test.performance_script import PerformanceScript
from automated_main.utils.http_format import response_success, response_failed
from django.conf import settings
import logging

logger = logging.getLogger('django')


class PerformanceScriptView(View):

    def get(self, request, performance_script_id, *args, **kwargs):
        """
        代表获取单个性能脚本
        :param request:
        :param performance_script_id:
        :param args:
        :param kwargs:
        :return:
        """

        performance_script = PerformanceScript.objects.filter(id=performance_script_id)
        performance_script_dict = PerformanceScript.objects.get(id=performance_script_id)

        logger.info(performance_script_dict.performance_script_name)

        jmeter_list = []
        for performance_scripts in performance_script:
            jmeter_script_name = os.path.basename(performance_scripts.performance_script).split('-')[-1]
            performance_jmeter_script_dict = {
                "url": performance_scripts.performance_script,
                "name": jmeter_script_name
            }

            jmeter_list.append(performance_jmeter_script_dict)

        if performance_script is None:
            return response_success()
        else:
            return response_success({"performance_script_name": performance_script_dict.performance_script_name,
                                     "performance_script_id": performance_script_dict.id,
                                     "performance_project_id": performance_script_dict.performance_project_id,
                                     "performance_script_url": jmeter_list})

    def post(self, request, performance_script_id, *args, **kwargs):
        """
        代表更改性能脚本
        :param request:
        :param performance_script_id:
        :param args:
        :param kwargs:
        :return:
        """
        performance_script = PerformanceScript.objects.filter(id=performance_script_id).first()
        if performance_script is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = PerformanceScriptForm(data)

        if form.is_valid():
            PerformanceScript.objects.filter(id=performance_script_id).update(**form.cleaned_data)
            return response_success("编辑性能脚本成功")
        else:
            raise MyException()

    def delete(self, request, performance_script_id, *args, **kwargs):
        """
        代表删除单独性能脚本
        :param request:
        :param performance_script_id:
        :param args:
        :param kwargs:
        :return:
        """

        PerformanceScript.objects.filter(id=performance_script_id).delete()
        return response_success("删除单独性能脚本")

    def put(self, request, *args, **kwargs):
        """
        代表创建性能脚本
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)

        form = PerformanceScriptForm(data)

        if form.is_valid():

            PerformanceScript.objects.create(**form.cleaned_data)
            return response_success("创建成功")
        else:
            raise MyException(message="创建失败")


class PerformanceProjectScriptView(View):

    def get(self, request, performance_project_id, *args, **kwargs):
        """
        获取 单个性能项目中包含得所有脚本
        :param performance_project_id:
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        performance_script = PerformanceScript.objects.filter(performance_project_id=performance_project_id)

        performance_script_list = []
        for performance_scripts in performance_script:

            if performance_scripts.performance_status == 0:
                status = "未执行"
            elif performance_scripts.performance_status == 1:
                status = "执行中"
            elif performance_scripts.performance_status == 2:
                status = "已完成"
            performance_script_dict = {
                "id": performance_scripts.id,
                "performance_project_name": performance_scripts.performance_project.performance_project_name,
                "performance_script_name": performance_scripts.performance_script_name,
                "performance_script": performance_scripts.performance_script,
                "performance_status": status,
                "updata_time": arrow.get(str(performance_scripts.updata_time)).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(str(performance_scripts.create_time)).format('YYYY-MM-DD HH:mm:ss'),
            }
            performance_script_list.append(performance_script_dict)

        if performance_script is None:
            return response_success()
        else:
            return response_success(performance_script_list)


class PerformanceScriptUpload(View):

    def post(self, request, *args, **kwargs):
        """
        上传脚本
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_obj = request.FILES.get("file")
        name = file_obj.name
        fn = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        fn = fn + '-%d' % random.randint(0, 100)

        path = os.path.join(settings.JMETER_ROOT, fn + '-' + name)

        with open(path, "wb") as f_write:
            for line in file_obj:
                f_write.write(line)

        return response_success({"file": "http://" + request.get_host() + "/jmeter_script/" + fn + '-' + name,
                                 "result": "OK",
                                 "fileName": name})


class PerformPerformanceScript(View):

    def get(self, request, performance_script_id, *args, **kwargs):
        """
        执行Jmeter脚本
        :param performance_script_id: 性能脚本ID
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if performance_script_id == "":
            return response_failed({"status": 10102, "message": "performance_script_id不能为空"})

        try:
            performance_script_tasks = PerformanceScript.objects.all()
            for t in performance_script_tasks:
                if t.performance_status == 1:
                    return response_failed({"status": 10200, "message": "当前有任务正在执行！"})

            performance_script = PerformanceScript.objects.get(id=performance_script_id)
            # 更改运行状态
            performance_script.performance_status = 1
            performance_script.save()

            performance_script_path = settings.JMETER_ROOT + "/" + os.path.basename(
                performance_script.performance_script)
            logger.info("脚本路径" + performance_script_path)
            fn = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            fn = str(performance_script.id) + "-" + fn + '-%d' % random.randint(0, 100)

            logger.info("性能脚本名称" + fn)

            ENV_PROFILE = os.getenv("ENV")
            if ENV_PROFILE == "SERVER":
                jmeter = 'jmeter.sh'
            elif ENV_PROFILE == "1":
                jmeter = 'jmeter'

            jmeter_script = jmeter + ' -n -t ' + performance_script_path + ' -l ' + settings.JMETER_REPORT + '/' + fn + '/' + fn + '.jtl'

            logger.info("性能脚本命令" + jmeter_script)

            os.system(jmeter_script)
            logger.info(os.system(jmeter_script))

            jmeter_script_html = jmeter + " -g " + settings.JMETER_REPORT + "/" + fn + "/" + fn + ".jtl" + " -e -o " + settings.JMETER_REPORT + "/" + fn + "/" + fn

            logger.info("性能脚本报告命令" + jmeter_script_html)
            os.system(jmeter_script_html)

            performance_script.performance_status = 2
            performance_script.save()
            result = "执行性能脚本成功"
        except Exception as e:
            result = e
            logger.info("这是报错" + e)

        return response_success(result)


class PerformanceScriptReport(View):

    def get(self, request, performance_script_id, *args, **kwargs):
        """
        查看测试报告
        :param request:
        :param performance_script_id: 性能脚本id
        :param args:
        :param kwargs:
        :return:
        """
        if performance_script_id == "":
            return response_failed({"status": 10102, "message": "performance_script_id不能为空"})

        dir = settings.JMETER_REPORT
        dir_list = os.listdir(dir)

        performance_script_report_list = []
        for report in dir_list:
            script_report = report.split('-')[0]
            if script_report == str(performance_script_id):
                logger.info("匹配" + script_report)
                performance_script_report_dict = {
                    "performance_script_report_name": report,
                    "performance_script_id": performance_script_id,
                    "file": "http://" + request.get_host() + "/jmeter_report/Report/" + report + "/" + report + "/" + "index.html"
                }

                performance_script_report_list.append(performance_script_report_dict)

            else:
                pass
        return response_success(performance_script_report_list)
