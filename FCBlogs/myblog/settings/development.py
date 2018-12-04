from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']  # 从环境变量中读取，增加安全性

# SECURITY WARNING: don't run with debug turned on in production!2.
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASE_PASSSWORD = os.environ['DATABASE_PASSSWORD']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myblogs',  # 要连接的数据库，连接前需要创建好
        'USER': 'root',  # 连接数据库的用户名
        'PASSWORD': DATABASE_PASSSWORD,  # 连接数据库的密码,在环境变量中配置
        'HOST': '127.0.0.1',  # 连接主机，默认本级
        'PORT': 3306  # 端口 默认3306
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = '1403179190@qq.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']  # 授权码
EMAIL_SUBJECT_PREFIX = u'[FCBlog]'
EMAIL_USE_SSL = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)
EMAIL_TIMEOUT = 60
FROM_EMAIL = 'FCBlog<1403179190@qq.com>'
