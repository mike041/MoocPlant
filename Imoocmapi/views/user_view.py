# coding=utf-8
from django.shortcuts import render, redirect

from ..models import UserInfo
from django.http import HttpResponseRedirect, HttpResponse
import json
import jwt


def check_login(func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("token",None)
        if token == 'null':
            return HttpResponseRedirect("/login/")
        else:
            try:
                jwt.decode(token, "sercet", algorithms=['HS256'])
                return func(request, *args, **kwargs)
            except jwt.InvalidTokenError:
                return HttpResponseRedirect("/login/")

    return wrapper



def login(request):
    if request.method == 'POST':
        data = {
            "code": 10000,
            "msg": "登录成功",
            "url": "/index/",
            "token": "",
            "nick_name":""
        }
        request_data = json.loads(request.body.decode("utf-8"))
        username = request_data.get("username")
        password = request_data.get("password")
        if UserInfo.objects.get_user_count(username, password) == 1:
            nick_name = UserInfo.objects.get_user_nick_name(username).get("nick_name")
            token = jwt.encode(request_data, "sercet")
            data["token"] = token
            data["nick_name"] = nick_name
            return HttpResponse(json.dumps(data))
        else:
            return render(request, "login.html")
    else:
        token = request.COOKIES.get("token", None)
        if token == 'null':
            return render(request, "login.html")
        else:
            try:
                jwt.decode(token, "sercet", algorithms=['HS256'])
                return HttpResponseRedirect("/")
            except jwt.InvalidTokenError:
                return HttpResponseRedirect("/login/")
        return render(request, "login.html")


def logout(request):
    return HttpResponseRedirect("/login/")


@check_login
def index(request):
    """
    首页
    :param request:
    :return:
    这里来展示ios、android 性能数据、内存、cpu使用
    """
    # project_num = ProjectInfo.objects.count()
    # module
    # if request.method is "POST":
    device_id = "00008101-00016C9E02F8001E"
    dict_data = {}
    return render(request, "index.html")
