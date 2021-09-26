# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/21 11:20
@Auth ： WangYingHao
@File ：user_url.py
@IDE ：PyCharm

"""
from django.urls import path
from automated_main.view.user.users_views import UsersView
from automated_main.view.user.user_info_view import UserInfoView
urlpatterns = [
    # 用户接口
    path("api/backend/users/", UsersView.as_view()),
    path("api/backend/users/info/", UserInfoView.as_view()),
]