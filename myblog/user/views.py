# -*- coding: utf-8 -*-
# @Time    : 18-11-7 下午4:12
# @Author  : Felix Wang

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegisterForm


def login(requests):
    # 如果是form表单提交验证登录
    if requests.method == 'POST':
        login_form = LoginForm(requests.POST)
        if login_form.is_valid():  # 验证是否通过
            # 因为在form表单验证过了，所以不用自己再验证
            user = login_form.cleaned_data.get('user')
            auth.login(requests, user)
            return redirect(requests.GET.get('from', reverse('home')))
        else:
            login_form.add_error(None, '用户名或密码不正确')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(requests, 'user/login.html', context)


def login_for_model(requests):
    login_form = LoginForm(requests.POST)

    # 如果是form表单提交验证登录
    if login_form.is_valid():  # 验证是否通过
        # 因为在form表单验证过了，所以不用自己再验证
        user = login_form.cleaned_data.get('user')
        auth.login(requests, user)

        data = {
            'status': 'SUCCESS',
        }
    else:
        data = {
            'status': 'ERROR',
        }
    return JsonResponse(data)


def register(requests):
    if requests.method == 'POST':
        reg_form = RegisterForm(requests.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']

            # 创建用户
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(requests, user)
            # 登录之后跳转
            return redirect(requests.GET.get('from', reverse('home')))
    else:
        reg_form = RegisterForm()

    context = {
        'reg_form': reg_form,
    }
    return render(requests, 'user/register.html', context)


def logout(requests):
    auth.logout(requests)
    return redirect(requests.GET.get('from', reverse('home')))


def user_info(requests):
    context = {}
    return render(requests, 'user/user_info.html', context)
