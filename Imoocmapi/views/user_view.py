# coding=utf-8
from django.shortcuts import render
import json

from ..models import UserInfo
from django.http import HttpResponseRedirect


def login(request):
    if request.is_ajax():
        request_data = json.loads(request.body.decode('utf-8'))
        username = request_data.get("username")
        password = request_data.get("password")
        print(request_data)
        user_num = UserInfo.objects.get_user_count(username, password)

        if user_num == 1:
            request.session["login_status"] = True
            request.session["now_account"] = username
            return HttpResponseRedirect("/index/")
        else:
            return render(request, "login.html")
    else:
        return render(request, "login.html")
