# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 18:06
# @Author  : wangyinghao
# @FileName: RequestHandler.py
# @Software: PyCharm
import requests


class RequestHandler:
    def __init__(self):
        """session管理器"""
        self.session = requests.session()

    def visit(self, method, url, **kwargs):
        return self.session.request(method=method, url=url, **kwargs)

    def close_session(self):
        """关闭session"""
        self.session.close()


if __name__ == '__main__':
    # 以下是测试代码
    # post请求接口
    url = 'http://10.10.102.92:8000/api/backend/users/'
    payload = {
        "username": "admin",
        "password": "Raydata666"
    }
    req = RequestHandler()
    login_res = req.visit("get", url, params=payload)
    print(login_res.text)
    requests.request("post",url)
