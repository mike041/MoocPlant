import json
from random import randrange

from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render

# Create your views here.




from Imoocmapi.models import UserInfo, Bug, ProjectInfo
from Imoocmapi.views.user_view import check_login


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













def imPerformance(request):
    '''
    :param request:
    :return:
    '''
    data = {
        "env": ["pre", "test"]
    }
    return render(request, "im_performance.html", context=data)


def chatPerformance(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "chat_performance.html")


def imChat(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "im_chat.html")


def envList(request):
    '''
    添加环境
    :param request:
    :return:
    '''
    return render(request, "env_list.html")
