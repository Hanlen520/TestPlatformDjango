# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 11:11
@Auth ： WangYingHao
@File ：api_test_task_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.api_automation.api_test_task.api_test_task_list_view import ApiTestTaskListView
from automated_main.view.api_automation.api_test_task.api_test_task_view import ApiTestTaskView, GetApiCaseTree, CheckApiResultList, CheckApiResult, PerformApiTask, CheckApiResultErrorList
urlpatterns = [
    # API任务管理
    path("api/backend/api_test_task/list/<int:api_project_id>/", ApiTestTaskListView.as_view()),
    path("api/backend/api_test_task/<int:api_test_task_id>/", ApiTestTaskView.as_view()),
    path("api/backend/api_test_task/", ApiTestTaskView.as_view()),
    path("api/backend/api_test_task/get_api_case_tree/<int:api_project_id>/", GetApiCaseTree.as_view()),
    path("api/backend/api_test_task/get_api_case_tree/<int:api_test_task_id>/", GetApiCaseTree.as_view()),

    # API任务管理-查看报告列表
    path("api/backend/api_test_task/check_result_list/<int:api_test_task_id>/", CheckApiResultList.as_view()),

    # API任务管理-查看单独测试报告
    path("api/backend/api_test_task/check_result/<int:api_test_result_id>/<int:size_page>/<int:page>/", CheckApiResult.as_view()),
    path("api/backend/api_test_task/check_result/<int:api_test_result_id>/", CheckApiResult.as_view()),
    path("api/backend/api_test_task/single_check_result/<int:api_test_case_result_id>/", CheckApiResult.as_view()),
    # 查看失败报告
    path("api/backend/api_test_task/check_result/error/<int:api_test_result_id>/<int:size_page>/<int:page>/", CheckApiResultErrorList.as_view()),

    # API任务管理-执行任务
    path("api/backend/api_test_task/perform_api_task/<int:api_test_task_id>/", PerformApiTask.as_view()),
]