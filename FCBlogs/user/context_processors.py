# -*- coding: utf-8 -*-
# @Time    : 18-11-25 下午2:55
# @Author  : Felix Wang

from .forms import LoginForm


def login_model_form(requests):
    return {'login_model_form': LoginForm()}
