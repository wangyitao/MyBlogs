# -*- coding: utf-8 -*-
# @Time    : 18-11-15 下午8:20
# @Author  : Felix Wang
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render_to_response


class My404(MiddlewareMixin):
    def process_response(self, request, response):
        if str(response.status_code) == '404':  # 判断状态吗是否为404，为404则返回自定义的404页面
            import random
            return render_to_response(random.choice(['my404/my404_1.html', 'my404/my404_2.html']))
        return response
