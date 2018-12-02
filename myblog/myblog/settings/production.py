from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']  # 从环境变量中读取，增加安全性

# SECURITY WARNING: don't run with debug turned on in production!2.
DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASE_PASSSWORD = os.environ['DATABASE_PASSSWORD']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myblogs',  # 要连接的数据库，连接前需要创建好
        'USER': 'root',  # 连接数据库的用户名
        'PASSWORD': DATABASE_PASSSWORD,  # 连接数据库的密码
        'HOST': '127.0.0.1',  # 连接主机，默认本级
        'PORT': 3306  # 端口 默认3306
    }
}

# 发送邮箱设置
MAIL_HOST = 'smtp.qq.com'  # smtp服务地址
EMAIL_PORT = 465  # 端口号
EMAIL_HOST_USER = '1403179190@qq.com'  # qq邮箱
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']  # 如果是qq邮箱的话该密码是配置qq邮箱的SMTP功能的授权码
FROM_WHO = 'FCBlog'  # 前缀
