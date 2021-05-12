# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 22:15
# @Author  : wangyinghao
# @FileName: my_exception.py
# @Software: PyCharm


class ErrorCode:
    SYSTEM = 10000
    DB = 20000
    COMMON = 30000
    UNKNOWN = 40000


class MyException(Exception):
    def __init__(self, code=ErrorCode.COMMON, message='参数错误'):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message

