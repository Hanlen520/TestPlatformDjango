# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 17:01
# @Author  : wangyinghao
# @FileName: test.py
# @Software: PyCharm
import sys
import json
import os, django
import re
import unittest
from ddt import ddt, file_data, unpack
import time
import xmlrunner
from os.path import dirname, abspath
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
BASE_PATH = BASE_DIR.replace("\\", "/")
sys.path.append(BASE_PATH)
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
print('ssssssssssss', rootPath)
sys.path.append(rootPath)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutomatedTestPlatform.settings")# project_name 项目名称
django.setup()
print("运行测试文件：", BASE_PATH)