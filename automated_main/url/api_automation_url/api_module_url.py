# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 11:10
@Auth ： WangYingHao
@File ：api_module_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.api_automation.api_module.api_module_list_view import ApiModuleListView
from automated_main.view.api_automation.api_module.api_module_view import ApiModuleView
from automated_main.view.api_automation.api_module.api_module_view import ApiProjectModuleView
urlpatterns = [

    # API模块
    path("api/backend/api_module/list/", ApiModuleListView.as_view()),
    path("api/backend/api_module/", ApiModuleView.as_view()),
    path("api/backend/api_module/<int:api_module_id>/", ApiModuleView.as_view()),

    # 获取 单个api项目中包含得所有模块
    path("api/backend/api_project/api_module/<int:api_project_id>/", ApiProjectModuleView.as_view()),
]
