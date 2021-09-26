from django.test import TestCase

# Create your tests here.
import os

# Default settings between dev and prd

ENV_PROFILE = os.getenv("ENV")
print(ENV_PROFILE)

print(type(ENV_PROFILE))



if ENV_PROFILE == "SERVER":
    # 生产环境地址
    # ALLOWED_HOSTS = ["10.10.10.137"]
    print(22222)
elif ENV_PROFILE == "1":

    # 测试环境地址
    # ALLOWED_HOSTS = ["10.10.12.92"]
    print(3333333333)