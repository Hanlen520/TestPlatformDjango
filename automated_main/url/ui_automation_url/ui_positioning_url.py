# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 10:21
@Auth ： WangYingHao
@File ：ui_positioning_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.ui_automation.ui_positioning.ui_positioning_list_view import UiElementPositioningListView
from automated_main.view.ui_automation.ui_positioning.ui_positioning_view import UIPositioningView
urlpatterns = [
    path("api/backend/ui_positioning/list/", UiElementPositioningListView.as_view()),
    path("api/backend/ui_positioning/", UIPositioningView.as_view()),
    path("api/backend/ui_positioning/<int:element_positioning_id>/", UIPositioningView.as_view()),]
