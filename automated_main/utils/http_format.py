# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 18:35
# @Author  : wangyinghao
# @FileName: http_format.py
# @Software: PyCharm
from django.http import JsonResponse
from automated_main.exception.my_exception import ErrorCode


def response_json(success, error_code, message, data):
    result = dict()
    result["success"] = success
    result["error"] = {
        "code": error_code,
        "message": message
    }
    result["data"] = data
    return JsonResponse(result, safe=False)


def response_success(data={}):

    return response_json(True, "", "", data)


def response_failed(code=ErrorCode.COMMON, message="参数错误"):

    return response_json(False, code, message, {})

