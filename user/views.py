from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.urls import reverse

from user.forms import RegisterForm, LoginForm
from user.models import User
from django.shortcuts import HttpResponseRedirect, render


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            password = make_password(form.cleaned_data['user_name'])
            email = form.cleaned_data['email']
            User.objects.create(username=username, password=password, email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            errors = form.errors
            return render((request, 'register.html',{'errors':errors}))


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))

        else:
            errors = form.errors
            return render(request,'login.html',{'errors': errors})


def user_center_info(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


# 退出
def logout(request):
    if request.method == 'GET':
        # 删除session中的键值对user_id
        del request.session['user_id']
        return HttpResponseRedirect(reverse('goods:index'))


# 收货地址
def user_site(request):
    if request.method == 'GET':
        return render(request, 'user_center_site.html')

    if request.method == 'POST':
        pass


