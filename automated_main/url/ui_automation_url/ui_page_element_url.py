# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 10:18
@Auth ： WangYingHao
@File ：ui_page_element_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.ui_automation.ui_page_element.ui_page_element_list_view import UIPageElementListView
from automated_main.view.ui_automation.ui_page_element.ui_page_element_view import UIPageElementView, GetUiPageSelectData

urlpatterns = [
    path("api/backend/ui_page_element/list/", UIPageElementListView.as_view()),
    path("api/backend/ui_page_element/", UIPageElementView.as_view()),
    path("api/backend/ui_page_element/<int:ui_page_id>/", UIPageElementView.as_view()),
    path("api/backend/ui_page_element/get_ui_page_select_data/", GetUiPageSelectData.as_view()),
]
