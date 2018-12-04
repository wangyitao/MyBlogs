# -*- coding: utf-8 -*-
# @Time    : 18-11-4 下午5:22
# @Author  : Felix Wang

from django.urls import path
from . import views

urlpatterns = [
    path('update_comment',views.update_commit,name='update_comment')
]
