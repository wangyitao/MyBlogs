# -*- coding: utf-8 -*-
# @Time    : 18-11-4 下午5:22
# @Author  : Felix Wang

from django.urls import path
from . import views
urlpatterns = [
    # name 表示别名
    path('<int:blog_pk>',views.blog_detail,name='blog_detail')
]

