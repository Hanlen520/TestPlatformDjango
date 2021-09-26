# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 10:04
@Auth ： WangYingHao
@File ：system_home_page_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.system_home_page.system_home_page_list_view import SystemHomePageListView

urlpatterns = [
    path("api/backend/system_home_page_list/", SystemHomePageListView.as_view()),
]
