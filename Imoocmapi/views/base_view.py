import json
from random import randrange

from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render
import datetime

# Create your views here.


from Imoocmapi.models import UserInfo, Bug, ProjectInfo
from Imoocmapi.utils.common import change_system_date
from Imoocmapi.views.user_view import chech_user_auth, check_login


@chech_user_auth
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


@chech_user_auth
def imPerformance(request):
    '''
    :param request:
    :return:
    '''
    data = {
        "env": ["pre", "test"]
    }
    return render(request, "im_performance.html", context=data)


@chech_user_auth
def chatPerformance(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "chat_performance.html")


@chech_user_auth
def interfacePerformance(request):
    """
    接口压测
    :param request:
    :return:
    """
    return render(request, "interfacePerformance.html")


@chech_user_auth
def imChat(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "im_chat.html")


@chech_user_auth
def envList(request):
    '''
    添加环境
    :param request:
    :return:
    '''
    return render(request, "env_list.html")


@chech_user_auth
def changeDate(request):
    """
    修改服务端时间
    :param request:
    :return:
    """
    if request.method == "POST":
        data = {
            "msg": "更新成功"
        }
        request_data = json.loads(request.body.decode("utf-8")).get("datetime")
        change_system_date(request_data)
        return HttpResponse(json.dumps(data))
    else:
        data = {
            "time": ""
        }
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["time"] = time_str
        return render(request, "change_date.html", data)
