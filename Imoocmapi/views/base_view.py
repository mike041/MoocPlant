import json
import os
import random
from random import randrange

import gevent
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render
import datetime

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Imoocmapi import utils
from Imoocmapi.utils.send_message import User
from Imoocmapi.views.user_view import chech_user_auth, check_login
from sdk.mind_im_server import IMServer


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


def gevent_run(func, env='test', phone_list='', ports=None, message_types=[1, ]):
    gevent_list = []
    for phone in phone_list:
        ge = gevent.spawn(func, env, phone=phone, ports=ports, message_type=message_types)
        gevent_list.append(ge)
    gevent.joinall(gevent_list)


def random_run(env, phone, ports, message_types):
    user = User(env, phone_number=phone)
    user.login()
    port = ports[random.randrange(0, len(ports), 1)]
    user.start(port=port, message_types=message_types)


@check_login
@chech_user_auth
def imPerformance(request):
    '''
    :param request:
    :return:
    '''
    if request.is_ajax():
        response_data = {
            "msg": "添加成功"
        }

        request_data = json.loads(request.body.decode('utf-8'))
        print('request_data', json.dumps(request_data))
        env = request_data.get("env")
        mode = request_data.get("mode")
        sender = request_data.get("sender")
        receiver = request_data.get("receiver")
        group = request_data.get("group")
        message_type = request_data.get("message_type")
        ports = request_data.get("server_num")

        # 1 开启服务
        server = IMServer(env)

        server.build_servers(ports)

        if mode == 'random':
            response_data = {
                "msg": "开发中"
            }
            if env == 'pre':
                print('当前是预发环境')
                json_data: dict = utils.parse_json_file(os.path.join('Imoocmapi/', 'userdata', 'user_cookie.json'))
            elif env == 'test':
                print('当前是测试环境')
                json_data: dict = utils.parse_json_file(os.path.join('Imoocmapi/', 'userdata', 'test_user_cookie.json'))
            return HttpResponse(json.dumps(response_data))
            user_list = list(json_data.keys())[20:25]
            gevent_run(random_run, env=env, phone_list=user_list, ports=ports, message_types=message_type)
        elif mode == 'assign':
            if sender == '':
                response_data = {
                    "msg": "发送者不能为空"
                }
                return HttpResponse(json.dumps(response_data))
            if receiver == '' and group == '':
                response_data = {
                    "msg": "至少填写一个接收者或群组"
                }
                return HttpResponse(json.dumps(response_data))
            return HttpResponse(json.dumps(response_data))
            user = User(env, sender)
            user.login()
            user.start(user_id=receiver, group_id=group, message_types=message_type, servers=server.servers)


    else:
        return render(request, "im_performance.html")


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
