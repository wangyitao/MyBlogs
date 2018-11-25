# -*- coding: utf-8 -*-
# @Time    : 18-11-4 下午5:22
# @Author  : Felix Wang

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # 登录
    path('logout/', views.logout, name='logout'),  # 登录
    path('login_for_model/', views.login_for_model, name='login_for_model'),  # 登录
    path('register/', views.register, name='register'),  # 登录
    path('user_info/', views.user_info, name='user_info'),  # 登录
]
