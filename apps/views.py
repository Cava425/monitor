from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from account.models import User
from account.models import Behaviour
from django.db.models import Count
from .forms import ChangePwForm
import base64
import time




@csrf_exempt
def uploadImg(request):
    if request.method == 'POST':
        info = request.POST['info']
        img = request.POST['img']
        jpg = base64.b64decode(img)
        datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        filename = './media/img/' + datetime + '.jpg'
        imgUrl = '/media/img/' + datetime + '.jpg'
        file = open(filename, 'wb')
        file.write(jpg)
        file.close()

        beha = Behaviour()
        beha.type = info
        # u_id = request.session.get('user_id')
        u_id = 1
        beha = Behaviour(type=info, img=imgUrl, user_id=u_id)
        beha.save()
    return HttpResponse("success")

def index(request):
    pass
    return render(request, 'index.html')


def welcome(request):
    if not request.session.get('is_login'):
        return redirect(reverse('account:login'))
    message = ""
    u_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=u_id)
        name = user.name
        email = user.email
        c_time = user.create_time
        year = time.localtime(time.time())[0]
        month = time.localtime(time.time())[1]
        num0 = Behaviour.objects.filter(type=0, user_id=u_id)
        num1 = Behaviour.objects.filter(type= 0, c_time__year=year, c_time__month=month, user_id=u_id)
        total_count = num0.count()
        month_count = num1.count()
        return render(request, 'welcome.html', {"message": message, "name": name, "email": email, "c_time": c_time, "total": total_count, "month": month_count})
    except User.DoesNotExist:
        message = "用户不存在！"
        return render(request, 'login.html', {"message": message})


def person_info(request):
    if not request.session.get('is_login'):
        return redirect(reverse('account:login'))
    message = ""
    u_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=u_id)
        name = user.name
        email = user.email
        c_time = user.create_time
        return render(request, 'info.html', {"message": message, "name": name, "email": email, "c_time": c_time})
    except User.DoesNotExist:
        message = "用户不存在！"
        return render(request, 'login.html', {"message": message})


def safe_setting(request):
    message = ""
    if not request.session.get('is_login'):
        message = "请登录后使用此功能！"
        render(request, 'login.html', {"message": message})
    if request.method == "POST":
        form = ChangePwForm(request.POST)
        if form.is_valid():
            password0 = form.cleaned_data['password0']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                message = "两次输入密码不一致！"
                return render(request, 'changePwd.html', {"message": message})
            u_id = request.session.get('user_id')
            try:
                user = User.objects.get(id=u_id)
                if user.password == password0:
                    user.password = password1
                    user.save()
                    message = "密码修改成功！"
                else:
                    message = "原密码输入错误！"
                    return render(request, 'changePwd.html', {"message": message})
            except User.DoesNotExist:
                message = "用户不存在！"
                return render(request, 'changePwd.html', {"message": message})
    return render(request, 'changePwd.html', {"message": message})


def bh_list(request):
    if not request.session.get('is_login'):
        return redirect(reverse('account:login'))
    message = ""
    u_id = request.session.get('user_id')
    behas = Behaviour.objects.filter(user_id=u_id).order_by('-c_time')
    user = User.objects.get(id=u_id)
    id = user.id
    name = user.name
    list = []
    for beha in behas:
        c_time = beha.c_time.strftime("%Y-%m-%d")
        if beha.type == 0:
            b_type = "坐姿不正确"
            b_url = beha.img
            list.append({"id": id, "name": name, "time": c_time, "type": b_type, "url": b_url})

    return render(request, 'bh-list.html', {"message": message, "list": list})


def line_chart(request):
    pass
    return render(request, 'echarts1.html')

@csrf_exempt
def echarts1(request):
    u_id = request.session.get('user_id')
    year = time.localtime(time.time())[0]
    month = time.localtime(time.time())[1]
    nums = Behaviour.objects.filter(type=0, c_time__year=year, c_time__month=month, user_id=u_id)\
        .extra(select={"c_time": "date_format(c_time, '%%e')"}).values('c_time')\
        .annotate(num=Count('c_time')).values('c_time', 'num')
    i = nums.count()
    list = []
    for num in nums:
        date_time = time.strftime('%Y-%m', time.localtime(time.time())) + "-" + str(num['c_time'])
        list.append({"d": date_time, "num": num['num']})
    return JsonResponse(list, safe=False)

def pie_chart(request):
    pass
    return render(request, 'echarts4.html')


@csrf_exempt
def echarts2(request):
    u_id = request.session.get('user_id')
    year = time.localtime(time.time())[0]
    month = time.localtime(time.time())[1]
    nums = Behaviour.objects.filter(c_time__year=year, c_time__month=month, user_id=u_id)\
        .extra(select={"c_time": "date_format(c_time, '%%e')"}).values('c_time')\
        .annotate(num=Count('c_time')).values('c_time', 'num')
    i = nums.count()
    list = []
    for num in nums:
        date_time = time.strftime('%Y-%m', time.localtime(time.time())) + "-" + str(num['c_time'])
        list.append({"name": date_time, "value": num['num'] * 10})
    return JsonResponse(list, safe=False)



