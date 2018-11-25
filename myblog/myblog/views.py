# -*- coding: utf-8 -*-
# @Time    : 18-11-7 下午4:12
# @Author  : Felix Wang

from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data, get_x_days_hot_data
from blog.models import Blog


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
