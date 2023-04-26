# coding=utf-8
import datetime
import time

from django.http import HttpResponse
from django.shortcuts import render
import json

from Imoocmapi.utils.common import change_system_date
from Imoocmapi.views.user_view import check_login, chech_user_auth


@check_login
@chech_user_auth
def interface_list(request):
    return render(request, "interface_list.html")


@check_login
@chech_user_auth
def add_interface(request):
    return render(request, "add_interface.html")


@chech_user_auth
def changeDate(request):
    """
    修改服务端时间
    :param request:
    :return:
    """
    if request.is_ajax():
        data = {
            "msg": "更新成功"
        }
        request_data = json.loads(request.body.decode("utf-8")).get("datetime")
        try:
            change_system_date(request_data)
        except Exception:
            data["msg"] = "更新失败"
        return HttpResponse(json.dumps(data))
    else:
        data = {
            "time": ""
        }
        time_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        #time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["time"] = time_str
        return render(request, "change_date.html", context=data)
