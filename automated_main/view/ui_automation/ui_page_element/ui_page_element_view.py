# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 15:31
# @Author  : wangyinghao
# @FileName: ui_page_element_view.py
# @Software: PyCharm
from django.views.generic import View
import json
from django.forms import model_to_dict
from automated_main.utils.http_format import response_success, response_failed
from automated_main.exception.my_exception import MyException
from automated_main.models.ui_automation.ui_page_element import UIPageElement
from automated_main.models.ui_automation.ui_page import UIPage
from automated_main.models.ui_automation.ui_project import UIProject
from automated_main.form.ui_page_element import UiPageElementForm


class UIPageElementView(View):

    def get(self, request, ui_page_id, *args, **kwargs):
        '''
        代表获取单个页面元素
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        page_element = UIPageElement.objects.filter(ui_page_id=ui_page_id)

        if page_element is None or len(page_element) == 0:
            return response_success([])
        else:
            page_and_project = UIPageElement.objects.filter(ui_page_id=ui_page_id).first()
            ui_page_element_data = []
            for ui_page_element in page_element:
                ui_page_element_dict = {
                    "ui_element_positioning_id": ui_page_element.ui_element_positioning.id,
                    "ui_page_element": ui_page_element.ui_page_element,
                    "ui_page_element_name": ui_page_element.ui_page_element_name,
                    "ui_page_element_id": ui_page_element.id
                }
                ui_page_element_data.append(ui_page_element_dict)

            return response_success({"ui_page_element_data": ui_page_element_data, "ui_project_id": page_and_project.ui_project.id, "ui_page_id": page_and_project.ui_page.id})

    def post(self, request, ui_page_id, *args, **kwargs):
        '''
        代表更改页面元素
        :param request:
        :param args:da
        :param kwargs:
        :return:
        '''

        page_element = UIPageElement.objects.filter(ui_page_id=ui_page_id)
        print(page_element)
        if page_element is None:
            return response_success()
        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)
        print(data)

        form = UiPageElementForm(data)

        if form.is_valid():
            edit_page_element_id_list = []
            for i in data["ui_page_element_data"]:
                ui_element_positioning_id = (i['ui_element_positioning_id'])
                ui_page_element = (i['ui_page_element'])
                ui_page_element_name = i['ui_page_element_name']
                try:
                    ui_page_element_data = UIPageElement.objects.get(id=i['ui_page_element_id'])
                    ui_page_element_data.ui_project.id = data['ui_project_id']
                    ui_page_element_data.ui_page.id = data['ui_page_id']
                    ui_page_element_data.ui_page_element_name = ui_page_element_name
                    ui_page_element_data.ui_page_element = ui_page_element
                    ui_page_element_data.ui_element_positioning_id = ui_element_positioning_id
                    ui_page_element_data.save()
                    edit_page_element_id_list.append(int(i['ui_page_element_id']))
                except Exception as e:
                    UIPageElement.objects.create(ui_project_id=data['ui_project_id'], ui_page_id=data['ui_page_id'],
                                                 ui_page_element_name=ui_page_element_name,
                                                 ui_page_element=ui_page_element,
                                                 ui_element_positioning_id=ui_element_positioning_id)
                    ui_page_element_id = UIPageElement.objects.last()
                    edit_page_element_id_list.append(int(ui_page_element_id.id))

            print(edit_page_element_id_list)

            page_element_all_id_list = []
            for i in page_element:
                page_element_all_id_list.append(int(i.id))
            print(page_element_all_id_list)

            # 调试
            # print(list(set(page_element_all_id_list).difference(set(edit_page_element_id_list))))
            delete_ui_page_elemnt_id = list(set(page_element_all_id_list).difference(set(edit_page_element_id_list)))

            print(delete_ui_page_elemnt_id)

            for delete_elemnt_id in delete_ui_page_elemnt_id:
                print(delete_elemnt_id)
                UIPageElement.objects.filter(id=delete_elemnt_id).delete()
            return response_success("编辑页面元素成功")
        else:
            raise MyException()

    def delete(self, request, ui_page_element_id, *args, **kwargs):
        '''
        代表删除页面元素
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        UIPageElement.objects.filter(id=ui_page_element_id).delete()
        return response_success("删除页面元素成功")

    def put(self, request, *args, **kwargs):
        '''
        代表创建页面元素
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        body = request.body
        if not body:
            return response_success()
        data = json.loads(body)
        print(data)
        form = UiPageElementForm(data)
        if form.is_valid():
            for i in data["ui_page_element_data"]:
                print(i)
                ui_element_positioning_id = (i['ui_element_positioning_id'])
                ui_page_element = (i['ui_page_element'])
                ui_page_element_name = i['ui_page_element_name']
                UIPageElement.objects.create(ui_project_id=data['ui_project_id'], ui_page_id=data['ui_page_id'], ui_page_element_name=ui_page_element_name, ui_page_element=ui_page_element, ui_element_positioning_id=ui_element_positioning_id)

            return response_success("创建页面元素成功")
        else:
            raise MyException()


class GetUiPageSelectData(View):
    def get(self, request, *args, **kwargs):
        """
        获取 "UI项目>UI页面" 列表
        :param request:
        :return: 项目接口列表
        """

        ui_projects = UIProject.objects.all()
        data_list = []
        for project in ui_projects:
            project_dict = {
                "project_id": project.id,
                "ui_project_name": project.ui_project_name
            }

            ui_pages = UIPage.objects.filter(ui_project_id=project.id)
            page_list = []
            for ui_page in ui_pages:
                page_list.append({
                    "ui_page_id": ui_page.id,
                    "ui_page_name": ui_page.ui_page_name,
                })

            project_dict["page_list"] = page_list
            # print(page_list)
            data_list.append(project_dict)
        print(data_list)

        return response_success(data_list)

