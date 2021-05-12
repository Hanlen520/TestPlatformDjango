# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 18:30
# @Author  : wangyinghao
# @FileName: my_middle_ware.py
# @Software: PyCharm
import traceback
from django.db import DatabaseError
from django.utils.deprecation import MiddlewareMixin
from automated_main.utils.http_format import response_success, response_failed
from automated_main.exception.my_exception import MyException, ErrorCode

# ALLOW_PATHS = ["/api/backend/users/info/", "/api/backend/users/", "/api/backend/ui_project/list/",
#                "/api/backend/ui_project/", "api/backend/ui_project/<int:ui_project_id>/"]

ALLOW_PATHS = []


class MyMiddleWare(MiddlewareMixin):

    def process_request(self, request): # 会捕捉所有得请求
        # print('请求进来了')
        current_path = request.path
        if current_path not in ALLOW_PATHS:
            pass
        else:
            user = request.user
            if user.is_authenticated:
                pass
            else:
                raise response_failed(ErrorCode.UNKNOWN, '未知错误')

        pass

    def process_response(self, request, response): #会捕捉所有得响应
        # print('响应来了')
        return response

    def process_exception(self, request, exception): #会捕捉到所有异常
        print('捕捉异常')
        print(traceback.print_exc())

        if isinstance(exception, MyException):
            print("这是我的错误")
            code = exception.code
            message = exception.message
            return response_failed(code, message)
        elif isinstance(exception, DatabaseError):
            print('数据库错误')
            return response_failed(ErrorCode.DB, '数据库错误')
        else:
            print('未知错误')
            return response_failed(ErrorCode.UNKNOWN, '未知错误')
