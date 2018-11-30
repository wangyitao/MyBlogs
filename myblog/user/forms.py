# -*- coding: utf-8 -*-
# @Time    : 18-11-20 下午8:10
# @Author  : Felix Wang

import re
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名', required=True,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'}))
    # widget指定input标签类型
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):  # 验证数据
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            # 使用邮箱登录
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user  # 将验证过的user放入clean_data
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

    verification_code = forms.CharField(
        label='验证码',
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入验证码',
            }
        )
    )

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

    def __init__(self, *args, **kwargs):
        if 'requests' in kwargs:
            self.requests = kwargs.pop('requests')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            raise forms.ValidationError('邮箱格式错误')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip().upper()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        code = self.requests.session.get('register_code', '').upper()
        if code != verification_code or code == '':
            raise forms.ValidationError('验证码不正确')
        return verification_code


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label='新的昵称',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入新的昵称',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    # 表单验证
    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('新的昵称不能为空')
        return nickname_new


class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入邮箱',
            }
        )
    )

    verification_code = forms.CharField(
        label='验证码',
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入验证码',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        if 'requests' in kwargs:
            self.requests = kwargs.pop('requests')
        super().__init__(*args, **kwargs)

    # 表单验证
    def clean(self):
        # 判断用户是否登录
        if self.requests.user.is_authenticated:
            self.cleaned_data['user'] = self.requests.user
        else:
            raise forms.ValidationError('用户尚未登录')

        # 判断用户是否已经绑定邮箱
        if self.requests.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        code = self.requests.session.get('bind_email_code', '').upper()
        verification_code = self.cleaned_data.get('verification_code', '').upper()
        if code != verification_code or code == '':
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            raise forms.ValidationError('邮箱格式错误')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip().upper()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧的密码',
                                   min_length=6,
                                   required=True,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': '请输入旧的密码'}))

    new_password = forms.CharField(label='新的密码',
                                   min_length=6,
                                   required=True,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}))

    new_password_again = forms.CharField(label='请再次输入新的密码',
                                         min_length=6,
                                         required=True,
                                         widget=forms.PasswordInput(
                                             attrs={'class': 'form-control', 'placeholder': '请再次输入新的密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 验证新密码是否一致
        new_password = self.cleaned_data.get('new_password', '').strip()
        new_password_again = self.cleaned_data.get('new_password_again', '').strip()
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '').strip()
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')

        return old_password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             min_length=3,
                             required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入绑定过的邮箱'}))

    verification_code = forms.CharField(
        label='验证码',
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入验证码',
            }
        )
    )
    new_password = forms.CharField(label='密码',
                                   min_length=6,
                                   required=True,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def __init__(self, *args, **kwargs):
        if 'requests' in kwargs:
            self.requests = kwargs.pop('requests')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip().upper()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        code = self.requests.session.get('forgot_password_code', '').upper()
        if code != verification_code or code == '':
            raise forms.ValidationError('验证码不正确')
        return verification_code
