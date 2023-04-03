#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
import json

from Imoocmapi.views.user_view import check_login
@check_login
def interface_list(request):
    return render(request, "interface_list.html")

@check_login
def add_interface(request):
    return render(request,"add_interface.html")