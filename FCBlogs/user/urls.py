# -*- coding: utf-8 -*-
# @Time    : 18-11-4 下午5:22
# @Author  : Felix Wang

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # 登录
    path('logout/', views.logout, name='logout'),  # 登录
    path('login_for_model/', views.login_for_model, name='login_for_model'),  # 登录
    path('register/', views.register, name='register'),  # 注册
    path('user_info/', views.user_info, name='user_info'),  # 用户信息
    path('change_nickname/', views.change_nickname, name='change_nickname'),  # 更改昵称
    path('bind_email/', views.bind_email, name='bind_email'),  # 更改昵称
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),  # 更改昵称
    path('change_password/', views.change_password, name='change_password'),  # 更改密码
    path('forgot_password/', views.forgot_password, name='forgot_password'),  # 更改密码
]
