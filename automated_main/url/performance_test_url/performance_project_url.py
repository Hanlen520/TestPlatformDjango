# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 11:04
@Auth ： WangYingHao
@File ：performance_project_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.performance_test.performance_project.performance_project_list_view import PerformanceProjectListView
from automated_main.view.performance_test.performance_project.performance_project_view import PerformanceProjectView
urlpatterns = [

    # 性能测试-性能项目
    path("api/backend/performance_test/performance_project_list/", PerformanceProjectListView.as_view()),
    path("api/backend/performance_test/performance_project/", PerformanceProjectView.as_view()),
    path("api/backend/performance_test/performance_project/<int:performance_project_id>/",
         PerformanceProjectView.as_view()),
]
