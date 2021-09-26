# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 10:18
@Auth ： WangYingHao
@File ：ui_page_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.ui_automation.ui_page.ui_page_list_view import UiPageListView
from automated_main.view.ui_automation.ui_page.ui_page_view import UiPageView, UiProjectPageView

urlpatterns = [
    path("api/backend/ui_page/list/", UiPageListView.as_view()),
    path("api/backend/ui_page/", UiPageView.as_view()),
    path("api/backend/ui_page/<int:ui_page_id>/", UiPageView.as_view()),

    # 获取 单个UI项目中包含得所有页面
    path("api/backend/ui_page_element/ui_project_page/<int:ui_project_id>/", UiProjectPageView.as_view()),
]


