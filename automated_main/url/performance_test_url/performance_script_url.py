# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 11:04
@Auth ： WangYingHao
@File ：performance_script_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.performance_test.performance_script.performance_script_list_view import PerformanceScriptListView
from automated_main.view.performance_test.performance_script.performance_script_view import PerformanceScriptView, PerformanceProjectScriptView, PerformanceScriptUpload, PerformPerformanceScript, PerformanceScriptReport

urlpatterns = [

    path("api/backend/performance_test/performance_script_list/", PerformanceScriptListView.as_view()),

    path("api/backend/performance_test/performance_script/", PerformanceScriptView.as_view()),
    path("api/backend/performance_test/performance_script/<int:performance_script_id>/",
         PerformanceScriptView.as_view()),

    # 获取 单个性能测试项目中包含得所有性能脚本
    path("api/backend/performance_test/performance_project_script/<int:performance_project_id>/",
         PerformanceProjectScriptView.as_view()),

    # 上传性能测试脚本
    path("api/backend/performance_test/performance_script_upload/", PerformanceScriptUpload.as_view(), name="upload"),

    # 执行性能脚本
    path("api/backend/performance_test/perform_performance_script/<int:performance_script_id>/",
         PerformPerformanceScript.as_view()),

    # 性能测试报告
    path("api/backend/performance_test/performance_script_report/<int:performance_script_id>/",
         PerformanceScriptReport.as_view()),


]


