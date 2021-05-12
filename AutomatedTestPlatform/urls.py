"""AutomatedTestPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from automated_main.view.user.users_views import UsersView
from automated_main.view.user.user_info_view import UserInfoView
from automated_main.view.ui_automation.ui_project.ui_project_view import UiProjectView
from automated_main.view.ui_automation.ui_project.ui_project_list_view import UiProjectListView
from automated_main.view.ui_automation.ui_page.ui_page_list_view import UiPageListView
from automated_main.view.ui_automation.ui_page.ui_page_view import UiPageView, UiProjectPageView
from automated_main.view.ui_automation.ui_positioning.ui_positioning_list_view import UiElementPositioningListView
from automated_main.view.ui_automation.ui_positioning.ui_positioning_view import UIPositioningView
from automated_main.view.ui_automation.ui_element_operation.ui_element_operation_list_view import UiElementOperationListView
from automated_main.view.ui_automation.ui_element_operation.ui_element_operation_view import UIElementOperationView
from automated_main.view.ui_automation.ui_page_element.ui_page_element_list_view import UIPageElementListView
from automated_main.view.ui_automation.ui_page_element.ui_page_element_view import UIPageElementView, GetUiPageSelectData
from automated_main.view.ui_automation.ui_test_case.ui_test_case_list_view import UITestCaseListView
from automated_main.view.ui_automation.ui_test_case.ui_test_case_view import UITestCaseView, GetUiTestCaseSelectData, UiTestCaseDeBug
from automated_main.view.ui_automation.ui_test_task.ui_test_task_list_view import UITestTaskListView
from automated_main.view.ui_automation.ui_test_task.ui_test_task_view import UITestTaskView, GetUiCaseTree, PerformUiTask, CheckResultList, CheckResult
from automated_main.view.api_automation.api_project.api_project_view import ApiProjectView
from automated_main.view.api_automation.api_project.api_project_list_view import ApiProjectListView
from automated_main.view.api_automation.api_module.api_module_list_view import ApiModuleListView
from automated_main.view.api_automation.api_module.api_module_view import ApiModuleView
from automated_main.view.api_automation.api_module.api_module_view import ApiProjectModuleView
from automated_main.view.api_automation.api_environment.api_environment_list_view import ApiEnvironmentListView
from automated_main.view.api_automation.api_environment.api_environment_view import ApiEnvironmentView
from automated_main.view.api_automation.api_test_case.api_test_case_list_view import ApiTestCaseListView
from automated_main.view.api_automation.api_test_case.api_test_case_view import ApiTestCaseView, ApiTestCaseDeBugView
from automated_main.view.api_automation.api_business_test.api_business_test_list_view import ApiBusinessTestListView
from automated_main.view.api_automation.api_business_test.api_business_test_view import GetApiBusinessTestSelectData, ApiBusinessTestView
from automated_main.view.api_automation.api_test_task.api_test_task_list_view import ApiTestTaskListView
from automated_main.view.api_automation.api_test_task.api_test_task_view import ApiTestTaskView, GetApiCaseTree, CheckApiResultList, CheckApiResult, PerformApiTask
from django.http.response import JsonResponse

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 用户接口
    path("api/backend/users/", UsersView.as_view()),
    path("api/backend/users/info/", UserInfoView.as_view()),


    # UI项目接口
    path("api/backend/ui_project/", UiProjectView.as_view()),
    path("api/backend/ui_project/<int:ui_project_id>/", UiProjectView.as_view()),
    path("api/backend/ui_project/list/", UiProjectListView.as_view()),

    # UI页面接口
    path("api/backend/ui_page/list/", UiPageListView.as_view()),
    path("api/backend/ui_page/", UiPageView.as_view()),
    path("api/backend/ui_page/<int:ui_page_id>/", UiPageView.as_view()),

    # UI页面元素
    path("api/backend/ui_page_element/list/", UIPageElementListView.as_view()),
    path("api/backend/ui_page_element/", UIPageElementView.as_view()),
    path("api/backend/ui_page_element/<int:ui_page_id>/", UIPageElementView.as_view()),
    path("api/backend/ui_page_element/get_ui_page_select_data/", GetUiPageSelectData.as_view()),
    # 获取 单个UI项目中包含得所有页面
    path("api/backend/ui_page_element/ui_project_page/<int:ui_project_id>/", UiProjectPageView.as_view()),


    # UI定位操作
    path("api/backend/ui_positioning/list/", UiElementPositioningListView.as_view()),
    path("api/backend/ui_positioning/", UIPositioningView.as_view()),
    path("api/backend/ui_positioning/<int:element_positioning_id>/", UIPositioningView.as_view()),

    # UI元素操作
    path("api/backend/ui_element_operation/list/", UiElementOperationListView.as_view()),
    path("api/backend/ui_element_operation/", UIElementOperationView.as_view()),
    path("api/backend/ui_element_operation/<int:element_operation_id>/", UIElementOperationView.as_view()),


    # UI测试用例
    path("api/backend/ui_test_case/list/<int:ui_project_id>/", UITestCaseListView.as_view()),
    path("api/backend/ui_test_case/", UITestCaseView.as_view()),
    path("api/backend/ui_test_case/<int:ui_test_case_id>/", UITestCaseView.as_view()),
    path("api/backend/ui_test_case/get_ui_test_case_select_data/", GetUiTestCaseSelectData.as_view()),
    path("api/backend/ui_test_case/debug_ui_test_case/", UiTestCaseDeBug.as_view()),

    # UI任务管理
    path("api/backend/ui_test_task/list/<int:ui_project_id>/", UITestTaskListView.as_view()),
    path("api/backend/ui_test_task/<int:ui_test_task_id>/", UITestTaskView.as_view()),
    path("api/backend/ui_test_task/", UITestTaskView.as_view()),
    path("api/backend/ui_test_task/get_ui_case_tree/<int:ui_project_id>/", GetUiCaseTree.as_view()),
    path("api/backend/ui_test_task/get_ui_case_tree/<int:ui_test_task_id>/", GetUiCaseTree.as_view()),

    # UI任务管理-执行任务
    path("api/backend/ui_test_task/perform_ui_task/<int:ui_test_task_id>/", PerformUiTask.as_view()),

    # UI任务管理-查看报告列表
    path("api/backend/ui_test_task/check_result_list/<int:ui_test_task_id>/", CheckResultList.as_view()),

    # UI任务管理-查看单独测试报告
    path("api/backend/ui_test_task/check_result/<int:ui_test_result_id>/", CheckResult.as_view()),



    # API项目
    path("api/backend/api_project/", ApiProjectView.as_view()),
    path("api/backend/api_project/<int:api_project_id>/", ApiProjectView.as_view()),
    path("api/backend/api_project/list/", ApiProjectListView.as_view()),


    # API模块
    path("api/backend/api_module/list/", ApiModuleListView.as_view()),
    path("api/backend/api_module/", ApiModuleView.as_view()),
    path("api/backend/api_module/<int:api_module_id>/", ApiModuleView.as_view()),

    # 获取 单个api项目中包含得所有模块
    path("api/backend/api_project/api_module/<int:api_project_id>/", ApiProjectModuleView.as_view()),


    # 获取api环境列表
    path("api/backend/api_environment/list/", ApiEnvironmentListView.as_view()),
    path("api/backend/api_environment/", ApiEnvironmentView.as_view()),
    path("api/backend/api_environment/<int:api_environment_id>/", ApiEnvironmentView.as_view()),

    # API测试用例
    path("api/backend/api_test_case/list/<int:api_module_id>/", ApiTestCaseListView.as_view()),
    path("api/backend/api_test_case/<int:api_test_case_id>/", ApiTestCaseView.as_view()),
    path("api/backend/api_test_case/", ApiTestCaseView.as_view()),
    path("api/backend/api_test_case/debug/", ApiTestCaseDeBugView.as_view()),

    # API业务测试
    path("api/backend/api_business_test/list/<int:api_project_id>/", ApiBusinessTestListView.as_view()),
    path("api/backend/api_business_test/get_api_test_business_test_select_data/<int:api_project_id>/", GetApiBusinessTestSelectData.as_view()),
    path("api/backend/api_business_test/", ApiBusinessTestView.as_view()),
    path("api/backend/api_business_test/<int:api_business_test_id>/", ApiBusinessTestView.as_view()),

    # API任务管理
    path("api/backend/api_test_task/list/<int:api_project_id>/", ApiTestTaskListView.as_view()),
    path("api/backend/api_test_task/<int:api_test_task_id>/", ApiTestTaskView.as_view()),
    path("api/backend/api_test_task/", ApiTestTaskView.as_view()),
    path("api/backend/api_test_task/get_api_case_tree/<int:api_project_id>/", GetApiCaseTree.as_view()),
    path("api/backend/api_test_task/get_api_case_tree/<int:api_test_task_id>/", GetApiCaseTree.as_view()),

    # API任务管理-查看报告列表
    path("api/backend/api_test_task/check_result_list/<int:api_test_task_id>/", CheckApiResultList.as_view()),

    # API任务管理-查看单独测试报告
    path("api/backend/api_test_task/check_result/<int:api_test_result_id>/", CheckApiResult.as_view()),
    path("api/backend/api_test_task/single_check_result/<int:api_test_case_result_id>/", CheckApiResult.as_view()),

    # API任务管理-执行任务
    path("api/backend/api_test_task/perform_api_task/<int:api_test_task_id>/", PerformApiTask.as_view()),


]
