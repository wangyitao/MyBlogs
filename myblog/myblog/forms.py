# -*- coding: utf-8 -*-
# @Time    : 18-11-20 下午8:10
# @Author  : Felix Wang

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    # widget指定input标签类型
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):  # 验证数据
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        self.cleaned_data.user = user  # 将验证过的user放入clean_data
        return self.cleaned_data


class RegisterForm(forms.Form):
    # 用户名字段
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    # 邮箱字段
    email = forms.EmailField(label='邮箱',
                             min_length=3,
                             required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    # 密码字段
    password = forms.CharField(label='密码',
                               min_length=6,
                               required=True,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    # 再次输入密码
    password_again = forms.CharField(label='确认密码',
                                     min_length=6,
                                     required=True,
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control', 'placeholder': '请再输入一次密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')

        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again


