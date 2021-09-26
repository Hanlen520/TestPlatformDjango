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
Including another URConf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
from automated_main.view.ui_automation.ui_test_case import ui_test_case_view

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 用户接口
    path('', include("automated_main.url.user_url.user_url")),

    # 系统首页
    path('', include("automated_main.url.system_home_page_url.system_home_page_url")),

    # UI项目接口
    path('', include("automated_main.url.ui_automation_url.ui_project_url")),

    # UI页面接口
    path('', include("automated_main.url.ui_automation_url.ui_page_url")),

    # UI页面元素
    path('', include("automated_main.url.ui_automation_url.ui_page_element_url")),

    # UI定位操作
    path('', include("automated_main.url.ui_automation_url.ui_positioning_url")),

    # UI元素操作
    path('', include("automated_main.url.ui_automation_url.ui_element_operation_url")),


    # UI测试用例
    path('', include("automated_main.url.ui_automation_url.ui_test_case_url")),

    # UI任务管理
    path('', include("automated_main.url.ui_automation_url.ui_test_task_url")),

    # API项目
    path('', include("automated_main.url.api_automation_url.api_project_url")),

    # API模块
    path('', include("automated_main.url.api_automation_url.api_module_url")),

    # 获取api环境列表
    path('', include("automated_main.url.api_automation_url.api_environment_url")),


    # API测试用例
    path('', include("automated_main.url.api_automation_url.api_test_case_url")),

    # API业务测试
    path('', include("automated_main.url.api_automation_url.api_business_test_url")),


    # API任务管理
    path('', include("automated_main.url.api_automation_url.api_test_task_url")),

    # 性能测试-性能项目
    path('', include("automated_main.url.performance_test_url.performance_project_url")),


    # 性能测试-测试脚本
    path('', include("automated_main.url.performance_test_url.performance_script_url")),

    # 上传文件地址 media配置——配合settings中的MEDIA_ROOT的配置，就可以在浏览器的地址栏访问media文件夹及里面的文件了
    url(r'jmeter_script/(?P<path>.*)', serve, {'document_root': settings.JMETER_ROOT}),


    # 性能测试报告地址
    url(r'jmeter_report/Report/(?P<path>.*)', serve, {'document_root': settings.JMETER_REPORT}),


]
