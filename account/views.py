from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import UserForm, RegisterForm
from .models import User


def login(request):
    if request.session.get('is_login', None):
        return redirect(reverse('apps:index'))
    if request.method == "POST":
        form = UserForm(request.POST)
        message = "请检查填写数据！"
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect(reverse('apps:index'))
                else:
                    message = "密码不正确！"
            except User.DoesNotExist:
                message = "用户名不存在！"
        return render(request, 'login.html', {"message": message})
    form = UserForm()
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(name=username)
            if user:
                message = '用户已经存在，请重新选择用户名！'
                return render(request, 'register.html', {"message": message})
            user = User.objects.filter(email=email)
            if user:
                message = '该邮箱地址已被注册，请使用别的邮箱！'
                return render(request, 'register.html', {"message": message})
            user = User.objects.create()
            user.name = username
            user.email = email
            user.password = password
            user.save()
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect(reverse('apps:index'))
    form = RegisterForm()
    return render(request, 'register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('account:login'))
    request.session.flush()
    return redirect(reverse('account:login'))

