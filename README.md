# TestPlatformDjango

# 根据数据库迁移文件生成对应SQL语句并执行
    python manage.py migrate
# 初次执行时为了先把默认Django需要的数据库创建出来,创建数据库迁移文件
    python manage.py makemigrations
# 启动Django
    python manage.py runserver 0.0.0.0:8081
