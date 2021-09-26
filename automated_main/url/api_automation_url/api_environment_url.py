# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 11:10
@Auth ： WangYingHao
@File ：api_environment_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.api_automation.api_environment.api_environment_list_view import ApiEnvironmentListView
from automated_main.view.api_automation.api_environment.api_environment_view import ApiEnvironmentView
urlpatterns = [

    # 获取api环境列表
    path("api/backend/api_environment/list/", ApiEnvironmentListView.as_view()),
    path("api/backend/api_environment/", ApiEnvironmentView.as_view()),
    path("api/backend/api_environment/<int:api_environment_id>/", ApiEnvironmentView.as_view()),
]