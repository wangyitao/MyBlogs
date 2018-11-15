# -*- coding: utf-8 -*-
# @Time    : 18-11-4 下午5:22
# @Author  : Felix Wang

from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    # name 表示别名
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    # 链接非常容易混掉，所以要区分，在链接前面添加type
    path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
    # 根据日期分类
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
]
