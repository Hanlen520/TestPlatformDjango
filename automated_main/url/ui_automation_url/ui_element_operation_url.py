# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 10:22
@Auth ： WangYingHao
@File ：ui_element_operation_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.ui_automation.ui_element_operation.ui_element_operation_list_view import UiElementOperationListView
from automated_main.view.ui_automation.ui_element_operation.ui_element_operation_view import UIElementOperationView
urlpatterns = [
    path("api/backend/ui_element_operation/list/", UiElementOperationListView.as_view()),
    path("api/backend/ui_element_operation/", UIElementOperationView.as_view()),
    path("api/backend/ui_element_operation/<int:element_operation_id>/", UIElementOperationView.as_view()),]