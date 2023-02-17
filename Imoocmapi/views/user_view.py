# coding=utf-8
from django.shortcuts import render

from ..models import UserInfo
from django.http import HttpResponseRedirect


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            request.session["login_status"] = True
            request.session["now_account"] = username
            return HttpResponseRedirect("/index/")
    else:
        return render(request, "login.html")
