# 前端VUE：
    Github地址：https://github.com/wangyinghaotest/VueAutomatedTestPlatform
# TestPlatformDjango
    先添加系统的环境变量 ENV=1 用来区别本地环境以及线上环境
    测试环境：ENV=1
    生产环境：ENV=SERVER

# 根据数据库迁移文件生成对应SQL语句并执行
    python manage.py migrate
# 初次执行时为了先把默认Django需要的数据库创建出来,创建数据库迁移文件
    python manage.py makemigrations
# 启动Django
    python manage.py runserver 0.0.0.0:8081
