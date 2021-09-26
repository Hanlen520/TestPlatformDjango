# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 10:20
@Auth ： WangYingHao
@File ：ui_test_case_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.ui_automation.ui_test_case.ui_test_case_list_view import UITestCaseListView
from automated_main.view.ui_automation.ui_test_case.ui_test_case_view import UITestCaseView, GetUiTestCaseSelectData, UiTestCaseDeBug
urlpatterns = [
    path("api/backend/ui_test_case/list/<int:ui_project_id>/", UITestCaseListView.as_view()),
    path("api/backend/ui_test_case/", UITestCaseView.as_view()),
    path("api/backend/ui_test_case/<int:ui_test_case_id>/", UITestCaseView.as_view()),
    path("api/backend/ui_test_case/get_ui_test_case_select_data/", GetUiTestCaseSelectData.as_view()),
    path("api/backend/ui_test_case/debug_ui_test_case/", UiTestCaseDeBug.as_view()),
]
