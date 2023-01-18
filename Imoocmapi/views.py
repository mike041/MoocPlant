import json
from random import randrange

from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render

# Create your views here.

from Imoocmapi.models import UserInfo


def login(request):
    if request.method is "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            request.session["login_status"] = True
            request.session["now_account"] = username
            return HttpResponseRedirect("/index/")
    else:
        return render(request, "login.html")


def check_login(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("login_status"):
            return HttpResponseRedirect("/login/")
        return func(request, *args, **kwargs)

    return wrapper


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


def projectList(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "project_list.html")


def addProject(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "add_project.html")


def moduleList(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "module_list.html")


def addModule(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "add_module.html")


def addVersion(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "add_version.html")


def versionList(request):
    '''
    :param request:
    :return:
    '''
    return render(request, "version_list.html")


def bugList(request):
    return render(request, 'bug_list.html')


def addBug(request):
    return render(request, 'add_bug.html')


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
