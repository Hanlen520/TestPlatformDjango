# -*- coding: utf-8 -*-
# @Time    : 2020/11/12 21:21
# @Author  : wangyinghao
# @FileName: user_info_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success, response_failed
from automated_main.exception.my_exception import MyException


class UserInfoView(View):
    def get(self, request, *args, **kwargs):
        '''
        代表获取用户的登录信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        user = request.user
        if user.is_authenticated:
            ret = {
                "username": user.username,
                "id": user.id,
            }
            return response_success(ret)
        else:
            raise MyException(message="用户没有登录")
