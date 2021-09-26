# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 11:11
@Auth ： WangYingHao
@File ：api_test_case_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.api_automation.api_test_case.api_test_case_list_view import ApiTestCaseListView
from automated_main.view.api_automation.api_test_case.api_test_case_view import ApiTestCaseView, ApiTestCaseDeBugView
urlpatterns = [
    # API测试用例
    path("api/backend/api_test_case/list/<int:api_module_id>/", ApiTestCaseListView.as_view()),
    path("api/backend/api_test_case/<int:api_test_case_id>/", ApiTestCaseView.as_view()),
    path("api/backend/api_test_case/", ApiTestCaseView.as_view()),
    path("api/backend/api_test_case/debug/", ApiTestCaseDeBugView.as_view()),
]