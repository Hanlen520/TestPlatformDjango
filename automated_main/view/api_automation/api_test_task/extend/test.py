# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 17:01
# @Author  : wangyinghao
# @FileName: test.py
# @Software: PyCharm
import pandas as pd
data = [
    {
        "ui_test_case_name": "密码登录",
        "ui_error": "0",
        "ui_successful": "1"
    },
    {
        "ui_test_case_name": "密码登录",
        "ui_error": "0",
        "ui_successful": "1"
    },
    {
        "ui_test_case_name": "密码登录",
        "ui_error": "1",
        "ui_successful": "0"
    },
    {
        "ui_test_case_name": "测试",
        "ui_error": "0",
        "ui_successful": "1"
    },
    {
        "ui_test_case_name": "测试2222",
        "ui_error": "0",
        "ui_successful": "1"
    }
]
# data = pd.DataFrame(data)
# data.ui_test_case_name.unique()



# data.drop_duplicates(['id','age'])



print(data)