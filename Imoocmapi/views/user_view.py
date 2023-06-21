# coding=utf-8
from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
import json
import jwt

from ..models import UserInfo, UserPermission, Bug


# from ..utils.common import handle_redis


def get_username(request):
    """
    根据用户获取项目信息
    :param request:
    :return:
    """
    token = request.COOKIES.get("token", None)
    user_data = jwt.decode(token, "sercet", algorithms=['HS256'])
    user_key = user_data.get("username")
    return user_key


def check_login(func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("token", None)
        if token == "null":
            return HttpResponseRedirect("/login/")
        else:
            try:
                user_data = jwt.decode(token, "sercet", algorithms=['HS256'])
                # user_key = user_data.get("username")
                # if handle_redis.get_value_str("token_" + user_key) is not None:
                return func(request, *args, **kwargs)
                # else:
                #    return HttpResponseRedirect("/login/")

            except jwt.InvalidTokenError:
                return HttpResponseRedirect("/login/")

    return wrapper


def chech_user_auth(func):
    def wrapper(request, *args, **kwargs):
        username = get_username(request)
        user_url_list = [url.get("system_url") for url in UserPermission.objects.get_user_permission(username)]
        user_request_url = request.path
        if user_request_url in user_url_list or "*" in user_url_list:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/no_auth/")

    return wrapper


def no_auth(request):
    return render(request, "noautth.html")


def login(request):
    data = {
        "code": 10000,
        "msg": "登录成功",
        "url": "/bug_list/",
        "token": "",
        "nick_name": ""
    }
    if request.method == 'POST':
        request_data = json.loads(request.body.decode("utf-8"))
        username = request_data.get("username")
        password = request_data.get("password")
        if UserInfo.objects.get_user_count(username, password) == 1:
            user_info = UserInfo.objects.get_user_nick_name(username)
            request_data["user_type"] = user_info.get("user_type")
            token = jwt.encode(request_data, "sercet")
            data["token"] = token
            data["nick_name"] = user_info.get("nick_name")
            # handle_redis.set_value("token_" + username, token)
            return HttpResponse(json.dumps(data))
        else:
            data["code"] = 10001
            data["msg"] = "用户名或密码错误"
            return HttpResponse(json.dumps(data))
            # data["msg"] = "请重新登录用户米"
            # return render(request, "login.html")
    else:
        token = request.COOKIES.get("token", None)
        if token == "null":
            return render(request, "login.html")
        else:
            try:
                jwt.decode(token, "sercet", algorithms=['HS256'])
                return HttpResponse(json.dumps(data))
            except jwt.InvalidTokenError:
                return render(request, "login.html")
        return render(request, "login.html")


def logout(request):
    return HttpResponseRedirect("/login/")


@check_login
@chech_user_auth
def index(request):
    """
    首页
    :param request:
    :return:
    这里来展示ios、android 性能数据、内存、cpu使用
    """

    UNSOLVED = 1
    LEGACY = 2
    SOLVED = 3
    # project_num = ProjectInfo.objects.count()
    # module
    # if request.method is "POST":
    device_id = "00008101-00016C9E02F8001E"
    token = request.COOKIES.get("token", None)
    user_data = jwt.decode(token, "sercet", algorithms=['HS256'])
    user_type = user_data.get("user_type", None)
    username = user_data.get("username", None)
    project_name = UserInfo.objects.get_project_name(username)
    data = {'user_name': username, 'user_type': user_type, 'project_name': project_name}
    key_list = ['未解决的bug数', '线上遗留bug数', '已解决待验证']
    data['statistics'] = UNSOLVED
    unsolved_num = len(Bug.objects.bug_statistics(data))
    data['statistics'] = LEGACY
    legacy_num = len(Bug.objects.bug_statistics(data))
    data['statistics'] = SOLVED
    solved_num = len(Bug.objects.bug_statistics(data))
    value_list = [unsolved_num, legacy_num, solved_num]

    if request.is_ajax():
        data = {
            "code": 10000,
            "msg": "获取成功",
            'key_list': key_list,
            'value_list': value_list
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    return render(request, "index.html")


@check_login
def get_developer(request):
    if request.is_ajax():
        data = {
            "developer_list": None,
            "msg": ""
        }
        project_name = get_project_name(request)[0]
        developer_list = UserInfo.objects.get_develop_user(project_name)
        data["developer_list"] = developer_list
        return HttpResponse(json.dumps(data))


def get_project_name(request):
    """
    根据用户获取项目名字
    :param request:
    :return:
    """
    username = get_username(request)
    project_name = UserInfo.objects.get_project_name(username)
    return project_name


def get_username(request):
    """
    根据用户获取项目信息
    :param request:
    :return:
    """
    token = request.COOKIES.get("token", None)
    user_data = jwt.decode(token, "sercet", algorithms=['HS256'])
    user_key = user_data.get("username")
    return user_key
