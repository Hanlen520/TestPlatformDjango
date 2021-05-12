# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 15:31
# @Author  : wangyinghao
# @FileName: ui_page_element_list_view.py
# @Software: PyCharm
from django.views.generic import View
from automated_main.utils.http_format import response_success, response_failed
from automated_main.models.ui_automation.ui_page_element import UIPageElement
import arrow


class UIPageElementListView(View):

    def get(self, request, *args, **kwargs):
        '''
        代表获取所有页面元素
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ui_page_element = UIPageElement.objects.all()
        ui_page_element_list = []

        for page_element in ui_page_element:
            _tz = 'Asia/Shanghai'
            page_element_dict = {
                "id": page_element.id,
                "ui_project_id": page_element.ui_project.id,
                "ui_project_name": page_element.ui_project.ui_project_name,
                "ui_page_id": page_element.ui_page.id,
                "ui_page_name": page_element.ui_page.ui_page_name,
                "ui_page_element_name": page_element.ui_page_element_name,
                "ui_page_element": page_element.ui_page_element,
                "ui_element_positioning_id": page_element.ui_element_positioning.id,
                "ui_element_positioning_name": page_element.ui_element_positioning.positioning_name,
                "updata_time": arrow.get(page_element.updata_time).to(_tz).format('YYYY-MM-DD HH:mm:ss'),
                "create_time": arrow.get(page_element.create_time).to(_tz).format('YYYY-MM-DD HH:mm:ss')
            }

            ui_page_element_list.append(page_element_dict)

        return response_success(ui_page_element_list)

