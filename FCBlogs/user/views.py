# -*- coding: utf-8 -*-
# @Time    : 18-11-7 下午4:12
# @Author  : Felix Wang
import random
import re
import time
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm
from .models import Profile


class Login(View):
    def get(self, requests):
        print('get')
        context = {
            'login_form': LoginForm(),
        }
        return render(requests, 'user/login.html', context)

    def post(self, requests):
        print('post')
        login_form = LoginForm(requests.POST)
        if login_form.is_valid():  # 验证是否通过
            # 因为在form表单验证过了，所以不用自己再验证
            user = login_form.cleaned_data.get('user')
            auth.login(requests, user)
            return redirect(requests.GET.get('from', reverse('home')))
        else:
            login_form.add_error(None, '用户名或密码不正确')
        context = {
            'login_form': login_form,
        }
        return render(requests, 'user/login.html', context)


# 登录模态框
class LoginForModel(View):
    def post(self, requests):
        login_form = LoginForm(requests.POST)

        # 如果是form表单提交验证登录
        if login_form.is_valid():  # 验证是否通过
            # 因为在form表单验证过了，所以不用自己再验证
            user = login_form.cleaned_data.get('user')
            auth.login(requests, user)

            data = {
                'status': 'SUCCESS',
            }
        else:
            data = {
                'status': 'ERROR',
            }
        return JsonResponse(data)


class Register(View):
    def get(self, requests):
        context = {
            'reg_form': RegisterForm(),
        }
        return render(requests, 'user/register.html', context)

    def post(self, requests):
        reg_form = RegisterForm(requests.POST, requests=requests)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']

            # 创建用户
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(requests, user)

            # 注册成功否删除保存的验证码
            del requests.session['register_code']

            # 登录之后跳转
            return redirect(requests.GET.get('from', reverse('home')))
        context = {
            'reg_form': reg_form,
        }
        return render(requests, 'user/register.html', context)


class Logout(View):
    def get(self, requests):
        auth.logout(requests)
        to = reverse('home')  # 登出，跳转到首页
        return redirect(to)


class UserInfo(View):
    def get(self, requests):
        context = {}
        return render(requests, 'user/user_info.html', context)


class ChangeNickname(View):
    def get(self, requests):
        redirect_to = requests.GET.get('from', reverse('home'))
        form = ChangeNicknameForm()
        context = {
            'submit_text': '修改',
            'page_title': '修改昵称',
            'form_title': '修改昵称',
            'form': form,
            'return_back_url': redirect_to,
        }
        return render(requests, 'form.html', context)

    def post(self, requests):
        redirect_to = requests.GET.get('from', reverse('home'))
        form = ChangeNicknameForm(requests.POST, user=requests.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=requests.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
        context = {
            'submit_text': '修改',
            'page_title': '修改昵称',
            'form_title': '修改昵称',
            'form': form,
            'return_back_url': redirect_to,
        }
        return render(requests, 'form.html', context)


class BindEmail(View):
    def get(self, requests):
        redirect_to = requests.GET.get('from', reverse('home'))
        form = BindEmailForm()

        context = {
            'submit_text': '绑定邮箱',
            'page_title': '绑定邮箱',
            'form_title': '绑定',
            'form': form,
            'return_back_url': redirect_to,
        }
        return render(requests, 'user/bind_email.html', context)

    def post(self, requests):
        redirect_to = requests.GET.get('from', reverse('home'))
        form = BindEmailForm(requests.POST, requests=requests)
        if form.is_valid():
            email = form.cleaned_data['email']
            requests.user.email = email
            requests.user.save()

            # 绑定成功后删除验证码
            del requests.session['bind_email_code']
            return redirect(redirect_to)
        context = {
            'submit_text': '绑定邮箱',
            'page_title': '绑定邮箱',
            'form_title': '绑定',
            'form': form,
            'return_back_url': redirect_to,
        }
        return render(requests, 'user/bind_email.html', context)


class SendVerificationCode(View):
    def get(self, requests):
        email = requests.GET.get('email', '')
        send_for = requests.GET.get('send_for', '')

        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            # 生成验证码
            all_codes = list(range(0x30, 0x39)) + list(range(0x61, 0x74)) + list(range(0x41, 0x5a))  # 大写，小写和数字
            code = ''.join([chr(random.choice(all_codes)) for i in range(6)])
            now = int(time.time())
            send_code_time = requests.session.get('send_code_time', 0)
            if now - send_code_time < 60:
                data = {
                    'status': 'ERROR',
                }
            else:
                requests.session[send_for] = code
                requests.session['send_code_time'] = send_code_time

                title = '验证码'
                text_content = '绑定邮箱'
                subject, from_email, to = title, settings.FROM_EMAIL, email
                html_content = """
                                <html>
                                  <head></head>
                                  <body>
                                    <p>Hi!<br>
                                       非常感谢您绑定邮箱！
                                       <br>
                                       本次的验证码是：{}，请不要透露给其他人！
                                       <br>
                                    </p>
                                    <img style="width:180px;height:240px" src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1541440161574&di=fd6156e441788866ffbd6c654d75fa23&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fblog%2F201507%2F22%2F20150722222322_Ky8Nj.jpeg" />
                                  </body>
                                </html>
                                """.format(code)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                data = {
                    'status': 'SUCCESS',
                    'msg': '邮件发送成功',
                }
        else:
            data = {
                'status': 'ERRORS',
                'msg': '邮箱格式不正确',
            }

        return JsonResponse(data)


class ChangePassword(View):
    def get(self, requests):
        redirect_to = reverse('home')
        form = ChangePasswordForm()

        context = {
            'submit_text': '修改',
            'page_title': '修改密码',
            'form_title': '修改密码',
            'form': form,
            'return_back_url': redirect_to,

        }
        return render(requests, 'form.html', context)

    def post(self, requests):
        redirect_to = reverse('home')
        form = ChangePasswordForm(requests.POST, user=requests.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            profile, created = Profile.objects.get_or_create(user=requests.user)
            profile.user.set_password(new_password)
            profile.user.save()
            # 密码修改成功后登出
            auth.logout(requests)
            return redirect(redirect_to)
        context = {
            'submit_text': '修改',
            'page_title': '修改密码',
            'form_title': '修改密码',
            'form': form,
            'return_back_url': redirect_to,

        }
        return render(requests, 'form.html', context)


class ForgotPassword(View):
    def get(self, requests):
        redirect_to = reverse('login')
        form = ForgotPasswordForm()

        context = {
            'submit_text': '重置密码',
            'page_title': '重置密码',
            'form_title': '重置',
            'form': form,
            'return_back_url': redirect_to,
        }
        return render(requests, 'user/forgot_password.html', context)

    def post(self, requests):
        redirect_to = reverse('login')
        form = ForgotPasswordForm(requests.POST, requests=requests)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # 绑定成功后删除验证码
            del requests.session['forgot_password_code']
            return redirect(redirect_to)
        context = {
            'submit_text': '重置密码',
            'page_title': '重置密码',
            'form_title': '重置',
            'form': form,
            'return_back_url': redirect_to,
        }
        return render(requests, 'user/forgot_password.html', context)
