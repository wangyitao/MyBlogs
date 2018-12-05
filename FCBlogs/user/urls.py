# -*- coding: utf-8 -*-
# @Time    : 18-11-4 下午5:22
# @Author  : Felix Wang

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),  # 登录
    path('logout/', views.Logout.as_view(), name='logout'),  # 登出
    path('login_for_model/', views.LoginForModel.as_view(), name='login_for_model'),  # 登录
    path('register/', views.Register.as_view(), name='register'),  # 注册
    path('user_info/', views.UserInfo.as_view(), name='user_info'),  # 用户信息
    path('change_nickname/', views.ChangeNickname.as_view(), name='change_nickname'),  # 更改昵称
    path('bind_email/', views.BindEmail.as_view(), name='bind_email'),  # 绑定邮箱
    path('send_verification_code/', views.SendVerificationCode.as_view(), name='send_verification_code'),  # 发送验证码
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),  # 更改密码
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),  # 忘记密码
]
