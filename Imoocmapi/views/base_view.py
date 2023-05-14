import json
from random import randrange

from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render
import datetime

# Create your views here.
from Imoocmapi.utils.send_message import User
from Imoocmapi.views.user_view import chech_user_auth
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

        env = request_data.get("env")
        mode = request_data.get("mode")
        sender = request_data.get("sender")
        receiver = request_data.get("receiver")
        group = request_data.get("group")
        message_type = request_data.get("message_type")
        server_num = request_data.get("server_num")

        # 1 开启服务
        server = IMServer(env)
        for port in range(30001, 30000 + server_num + 1):
            server.build_server(str(port))

        # 关闭所有服务
        # server.quit()

        if mode == 'random':
            response_data = {
                "msg": "开发中"
            }
            return HttpResponse(json.dumps(response_data))
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
            user = User(env, sender)
            user.login()
            user.start(user_id=receiver, group_id=group, message_types=message_type)

        # server.quit()

        return HttpResponse(json.dumps(response_data))
    else:
        return render(request, "add_project.html")


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
