# -*- coding: utf-8 -*-
# @Time    : 18-11-23 下午4:25
# @Author  : Felix Wang


from django.urls import path
from . import views

urlpatterns = [
    path('like_change', views.like_change, name='like_change'),
]
