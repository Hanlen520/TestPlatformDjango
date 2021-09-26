# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 11:11
@Auth ： WangYingHao
@File ：api_project_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.api_automation.api_project.api_project_view import ApiProjectView
from automated_main.view.api_automation.api_project.api_project_list_view import ApiProjectListView
urlpatterns = [

    # API项目
    path("api/backend/api_project/", ApiProjectView.as_view()),
    path("api/backend/api_project/<int:api_project_id>/", ApiProjectView.as_view()),
    path("api/backend/api_project/list/", ApiProjectListView.as_view()),]