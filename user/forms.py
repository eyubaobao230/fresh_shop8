import re

from django import forms
from django.contrib.auth.hashers import check_password

import user
from user.models import User


# 注册校验
class RegisterForm(forms.Form):
    user_name = forms.CharField(max_length=20,
                                min_length=2,
                                required=True,
                                error_messages={
                                    'required': '用户名必填',
                                    'max_length': '名字超过20太长了',
                                    'min_length':'用户名不能低于2'
                                })
    pwd = forms.CharField(max_length=20,
                                min_length=2,
                                required=True,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '密码超过20太长了',
                                    'min_length':'密码不能低于2'
                                })
    cpwd = forms.CharField(max_length=20,
                                min_length=2,
                                required=True,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '密码超过20太长了',
                                    'min_length':'密码不能低于2'
                                })
    email = forms.CharField(required=True,
                                error_messages={
                                    'required': '邮箱必填',
                                })
    allow = forms.CharField(required=True,
                                error_messages={
                                    'required': '必填同意',
                                })

    # 效验用户名
    def clean_user_name(self):
        # 效验注册的账号是否存在
        username = self.cleaned_data['user_name']
        user = User.objects.filter(username=username).first()

        if user:
            raise forms.ValidationError('账号已存在了')
        return self.cleaned_data['user_name']

    # 效验密码
    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致'})
        return self.cleaned_data

     # 效验邮箱
    def clean_email(self):
        email_re = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
        email = self.cleaned_data['email']
        if not re.match(email_re, email):
            raise forms.ValidationError('邮箱错误')
        return self.cleaned_data


# 登录效验
class LoginForm(forms.Form):
    username = forms.CharField(
                                required=True,
                                error_messages={
                                    'required': '用户名必填',

                                })
    pwd = forms.CharField(
                                required=True,
                                error_messages={
                                    'required': '密码必填',

                                })

    def clean(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()

        if not user:
            raise forms.ValidationError({'username':'账号不存在'})

        password = self.cleaned_data.get('pwd')
        if not check_password(password, user.password):
            raise forms.ValidationError({'pwd':'密码错误'})
        return self.cleaned_data


class AddressForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2,
                                required=True, error_messages={
                                'required': '姓名必填',
                                'max_length': '不能超过20',
                                'min_length': '姓名不能少于2'
                                })
    address = forms.CharField(max_length=20, min_length=2,
                                required=True, error_messages={
                                'required': '地址必填',
                                'max_length': '不能超过20',
                                'min_length': '地址不能少于2'
                                })
    postcode = forms.CharField(max_length=20, min_length=2,
                                required=True, error_messages={
                                'required': '邮箱必填',
                                'max_length': '不能超过20',
                                'min_length': '邮箱不能少于2'
                                })
    mobile = forms.CharField(max_length=11, min_length=1,
                                required=True, error_messages={
                                'required': '手机必填',
                                'max_length': '不能超过11',
                                'min_length': '手机不能少于1'
                                })







