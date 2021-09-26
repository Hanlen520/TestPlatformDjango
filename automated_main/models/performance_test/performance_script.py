# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/27 10:51
@Auth ： WangYingHao
@File ：performance_script.py
@IDE ：PyCharm

"""
from django.db import models
from automated_main.models.performance_test.performance_project import PerformanceProject
import time


def upload_to(instance, fielname):
    # 后缀
    sub = fielname.split('.')[-1]
    t = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return 'jmeter_script/namespace/%s.%s' % (t,sub,)


# Create your models here.
class PerformanceScript(models.Model):
    """
    性能测试脚本
    """
    performance_script_name = models.CharField("性能测试脚本名称", max_length=50, null=False)
    performance_project = models.ForeignKey(PerformanceProject, on_delete=models.CASCADE, null=True)
    performance_script = models.CharField("性能测试脚本", max_length=5000, null=False)
    performance_status = models.IntegerField("性能脚本运行状态", default=0)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.performance_script_name
