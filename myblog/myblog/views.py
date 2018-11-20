# -*- coding: utf-8 -*-
# @Time    : 18-11-7 下午4:12
# @Author  : Felix Wang

from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from read_statistics.utils import get_seven_days_read_data, get_x_days_hot_data
from blog.models import Blog
from .forms import LoginForm, RegisterForm


def home(requests):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    context = {
        'read_nums': read_nums,
        'dates': dates,
        'today_hot_data': get_x_days_hot_data(0),  # 获取今日热门
        'yesterday_hot_data': get_x_days_hot_data(1),  # 获取昨日热门
        'seven_days_hot_data': get_x_days_hot_data(7),  # 获取周热门
        'one_month_hot_data': get_x_days_hot_data(30),  # 获取月热门
    }
    return render(requests, 'home.html', context)


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
    return render(requests, 'login.html', context)


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
    return render(requests, 'register.html', context)
