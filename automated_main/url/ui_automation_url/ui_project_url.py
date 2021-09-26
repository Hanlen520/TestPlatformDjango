# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 10:17
@Auth ： WangYingHao
@File ：ui_project_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.ui_automation.ui_project.ui_project_view import UiProjectView
from automated_main.view.ui_automation.ui_project.ui_project_list_view import UiProjectListView

urlpatterns = [
    path("api/backend/ui_project/", UiProjectView.as_view()),
    path("api/backend/ui_project/<int:ui_project_id>/", UiProjectView.as_view()),
    path("api/backend/ui_project/list/", UiProjectListView.as_view()),
]
