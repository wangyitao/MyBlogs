# -*- coding: utf-8 -*-
# @Time    : 18-11-7 下午4:12
# @Author  : Felix Wang

from django.shortcuts import render_to_response


def home(requests):
    return render_to_response('home.html', {})
