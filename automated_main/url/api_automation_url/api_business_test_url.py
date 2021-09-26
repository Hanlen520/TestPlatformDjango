# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 11:10
@Auth ： WangYingHao
@File ：api_business_test_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.api_automation.api_business_test.api_business_test_list_view import ApiBusinessTestListView
from automated_main.view.api_automation.api_business_test.api_business_test_view import GetApiBusinessTestSelectData, ApiBusinessTestView
urlpatterns = [
    # API业务测试
    path("api/backend/api_business_test/list/<int:api_project_id>/", ApiBusinessTestListView.as_view()),
    path("api/backend/api_business_test/get_api_test_business_test_select_data/<int:api_project_id>/",
         GetApiBusinessTestSelectData.as_view()),
    path("api/backend/api_business_test/", ApiBusinessTestView.as_view()),
    path("api/backend/api_business_test/<int:api_business_test_id>/", ApiBusinessTestView.as_view()),
]