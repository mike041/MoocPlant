import json
import os
import random

import gevent
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Imoocmapi.utils import task_kill
from Imoocmapi.utils.send_message import User, Performance
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

        if mode == 'random':
            pass
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

        senders = str(sender).split(',')
        receivers = str(receiver).split(',')
        groups = str(group).split(',')
        performance = Performance(env)
        print('===================================================================================================')
        print(env)
        print(senders)
        print(receivers)
        print(groups)
        print(message_type)

        performance.process_run(senders=senders, ports=ports, receivers=receivers, groups=groups,
                                message_types=message_type,
                                )
        response_data['server_pids'] = ','.join(performance.server_pids)

        response_data['user_pids'] = ','.join(performance.user_pids)
        return HttpResponse(json.dumps(response_data))
    else:
        return render(request, "im_performance.html")


@check_login
@chech_user_auth
def taskkill(request):
    '''
    :param request:
    :return:
    '''
    if request.is_ajax():
        response_data = {
            "msg": "执行成功"
        }
        request_data = json.loads(request.body.decode('utf-8'))
        server_pids = [] if request_data.get('server_pids') == '' else request_data.get('server_pids').split(',')
        user_pids = [] if request_data.get('user_pids') == '' else request_data.get('user_pids').split(',')

        task_kill(user_pids)
        task_kill(server_pids)
        return HttpResponse(json.dumps(response_data))


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
