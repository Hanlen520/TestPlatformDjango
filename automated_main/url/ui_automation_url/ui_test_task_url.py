# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 10:21
@Auth ： WangYingHao
@File ：ui_test_task_url.py
@IDE ：PyCharm

"""
from django.urls import path
from django.urls import re_path
from django.views.static import serve
from AutomatedTestPlatform.settings import WEB_ROOT
from automated_main.view.ui_automation.ui_test_task.ui_test_task_list_view import UITestTaskListView
from automated_main.view.ui_automation.ui_test_task.ui_test_task_view import UITestTaskView, GetUiCaseTree, PerformUiTask, CheckResultList, CheckResult, DownloadWebScript, DownloadWebScriptTemplate
urlpatterns = [
    # UI任务管理
    path("api/backend/ui_test_task/list/<int:ui_project_id>/", UITestTaskListView.as_view()),
    path("api/backend/ui_test_task/<int:ui_test_task_id>/", UITestTaskView.as_view()),
    path("api/backend/ui_test_task/", UITestTaskView.as_view()),
    path("api/backend/ui_test_task/get_ui_case_tree/<int:ui_project_id>/", GetUiCaseTree.as_view()),
    path("api/backend/ui_test_task/get_ui_case_tree/<int:ui_test_task_id>/", GetUiCaseTree.as_view()),

    # UI任务管理-执行任务
    path("api/backend/ui_test_task/perform_ui_task/<int:ui_test_task_id>/", PerformUiTask.as_view()),

    # UI任务管理-查看报告列表
    path("api/backend/ui_test_task/check_result_list/<int:ui_test_task_id>/", CheckResultList.as_view()),

    # UI任务管理-删除单独测试报告
    path("api/backend/ui_test_task/check_result_list/<int:ui_test_task_id>/<int:ui_test_result_id>/", CheckResultList.as_view()),

    # UI任务管理-查看单独测试报告
    path("api/backend/ui_test_task/check_result/<int:ui_test_result_id>/", CheckResult.as_view()),

    # UI任务管理-查看单独测试报告异常详情
    path("api/backend/ui_test_task/check_result/ui_test_abnormal/<int:ui_test_abnormal_result_id>/", CheckResult.as_view()),

    # 下载web自动化脚本
    path("api/backend/ui_test_task/check_result/ui_test_web_script/<int:ui_test_result_id>/",
         DownloadWebScript.as_view()),

    # 下载web脚本模板
    path("api/backend/ui_test_task/check_result/ui_test_web_script/download_web_script_template/", DownloadWebScriptTemplate.as_view()),

    re_path('^web_log/test_log/(?P<path>.*)$', serve, {'document_root': WEB_ROOT}),

]
