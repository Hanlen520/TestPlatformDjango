# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 18:12
# @Author  : wangyinghao
# @FileName: ui_positioning_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success
from automated_main.models.ui_automation.ui_element_positioning import UIPositioning
import arrow


class UiElementPositioningListView(View):

    def get(self, request, *args, **kwargs):
        '''
        代表获取所有定位方法
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        data = request.GET
        size = int(data.get('size', 10))
        page = int(data.get('page', 1))
        ui_element_positioning = UIPositioning.objects.all()
        ui_element_positioning_list = []

        for element_positioning in ui_element_positioning:
            _tz = 'Asia/Shanghai'
            element_positioning_dict = {
                "id": element_positioning.id,
                "positioning_name": element_positioning.positioning_name,
                "locating_method": element_positioning.locating_method,
                "describe": element_positioning.describe,
                "updata_time": arrow.get(element_positioning.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(element_positioning.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss')
            }

            ui_element_positioning_list.append(element_positioning_dict)

        return response_success(ui_element_positioning_list)

