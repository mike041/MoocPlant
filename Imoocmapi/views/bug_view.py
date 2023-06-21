# coding=utf-8
import jwt
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import json

from .user_view import check_login, chech_user_auth, get_project_name
from ..models import Bug, ProjectInfo, ModuleInfo, Version, UserInfo
from ..utils.common import robot_message
from ..utils.tencent_cos import TencentCOS
import os
import datetime
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


def put_png(request):
    '''
    :param request:
    :return:
    '''
    if request.is_ajax():
        upload_image = request.FILES.get("files")
        media_root = settings.MEDIA_ROOT
        if not upload_image:
            return HttpResponse(json.dumps({
                'success': 0,
                'message': "未获取到要上传的图片",
                'url': ""
            }))

            # image format check
        file_name_list = upload_image.name.split('.')
        file_extension = file_name_list.pop(-1)
        file_name = '.'.join(file_name_list)

        # image floder check
        file_path = os.path.join(media_root, 'images', 'bug')
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as err:
                return HttpResponse(json.dumps({
                    'success': 0,
                    'message': "上传失败：%s" % str(err),
                    'url': ""
                }))

        # 图片重命名
        file_full_name = '%s_%s.%s' % (file_name,
                                       '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()),
                                       file_extension)

        # 把文件写入本地
        with open(os.path.join(file_path, file_full_name), 'wb+') as file:
            for chunk in upload_image.chunks():
                file.write(chunk)

        url = os.path.join(settings.MEDIA_URL, 'images/bug', file_full_name)
        # 上传的文件：绝对路径
        local_file = file_path + '/' + file_full_name
        img = Image.open(local_file)
        img_size = img.size
        width = str(img_size[0])
        height = str(img_size[1])  # 将原始文件名作为key传给COS
        key = 'mooc plant/' + file_full_name
        # 调用COS上传文件，返回url
        upload = TencentCOS().upload_cos(local_file, key) + "#" + width + "*" + height
        file_list = [upload]
        return HttpResponse(json.dumps({'success': 1,
                                        'message': "上传成功！",
                                        'data': file_list
                                        }))


@check_login
@chech_user_auth
def bugList(request):
    page = None
    platformItem = {"1": "IOS", "2": "Android", "3": "web", "4": "pc", "5": "pad", "6": "服务端"}
    start_level = {'1': '1星', '2': '2星', '3': '3星', '4': '4星'}
    bug_state = {'1': '未解决', '2': '已解决', '3': '延期解决', '4': '不解决', '5': '关闭', '6': '激活'}
    project_name = get_project_name(request)

    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))

        data['project'] = project_name
        token = request.COOKIES.get("token", None)
        user_data = jwt.decode(token, "sercet", algorithms=['HS256'])
        user_type = user_data.get("user_type", None)
        username = user_data.get("username", None)
        data["search_versions"] = data.get("search_versions", None)
        page = data.get("page", 1)
        # data.pop("page")
        if "only_me" in data.keys():
            data["buger"] = username

        else:
            data["only_me"] = "0"
        bug_list = Bug.objects.search_bug(data)
    else:
        bug_list = Bug.objects.get_all_bug(project_name)
    project_list = project_name
    for bug in bug_list:
        bug_png_list = []
        bug['plantform'] = platformItem[bug.get("plantform")]
        bug['state'] = bug_state[bug.get('state')]
        bug['start'] = start_level[bug.get("start")]
        bug_png = bug['png']
        if bug_png is not None and bug_png != "":
            bug_png_list = eval(bug_png)
            bug['png'] = bug_png_list
            bug['png_size'] = 60 * len(bug_png_list)
        # if bug["project__project_name"] not in project_list:
        #    project_list.append(bug["project__project_name"])
    # 分页

    if request.method == "GET":
        paginator = Paginator(bug_list, 10)
        page = request.GET.get("page", 1)
    else:
        paginator = Paginator(bug_list, 50)
    current_page = int(page)
    try:
        # 获取查询页数的接口数据列表，page()函数会判断page实参是否是有效数字。page()函数源码附在文章的最后
        apitest_list = paginator.get_page(current_page)
    except PageNotAnInteger:
        apitest_list = paginator.page(1)
    except (EmptyPage, InvalidPage):
        # paginator.num_pages
        apitest_list = paginator.page(paginator.num_pages)
    # 分页结束

    # todo 新增模块和版本数据用于筛选
    module_list = ModuleInfo.objects.get_module_name(project_name[0])
    version_list = Version.objects.get_project_version(project_name[0])
    bug_info = {
        "bug_info": apitest_list,  # bug_list,
        "project_list": project_list,
        "module_list": [module.get('module_name') for module in module_list],
        "version_list": [version.get('version') for version in version_list],
        "platform_item": platformItem,
        "bug_state": bug_state

    }
    if request.is_ajax():
        bug_info["bug_info"] = list(bug_info.get("bug_info"))
        return HttpResponse(json.dumps(bug_info))
    else:
        return render(request, 'bug_list.html', bug_info)


@check_login
@chech_user_auth
def addBug(request):
    if request.is_ajax():
        module_info = {
            "module": None
        }
        request_data = json.loads(request.body.decode('utf-8'))
        project_name = request_data.get("project")
        module_list = ModuleInfo.objects.get_module_name(project_name)
        module_info['module'] = module_list
        module_name = request_data.get("module")
        version = request_data.get("version")
        if module_name == "请选择":
            versionandmodule = {
                "module_list": None,
                "version_list": None
            }
            version_list = Version.objects.get_project_version(project_name)
            versionandmodule["version_list"] = version_list
            versionandmodule["module_list"] = module_list
            return HttpResponse(json.dumps(versionandmodule))
        elif version == "请选择":
            version_info = {
                "version_list": None
            }
            version_list = Version.objects.get_project_version(project_name)
            version_info["version_list"] = version_list
            return HttpResponse(json.dumps(version_info))
        else:
            # try:
            data = {
                "msg": "添加成功"
            }
            developer_name = request_data.get("developer")
            token = request.COOKIES.get("token")
            user_data = jwt.decode(token, "sercet", algorithms=['HS256'])
            tester = user_data.get("username")
            project_object = ProjectInfo.objects.get_project_by_name(project_name=project_name)
            module_object = ModuleInfo.objects.get_module(project_name=project_name, module_name=module_name)
            version_object = Version.objects.get_version(project_name=project_name, version=version)
            developer_object = UserInfo.objects.get_user_by_user_name(nick_name=developer_name)
            buger_object = UserInfo.objects.get_user_by_user_name(user_name=tester)
            request_data['project'] = project_object
            request_data['module'] = module_object
            request_data['version'] = version_object
            request_data['developer'] = developer_object
            request_data['buger'] = buger_object
            Bug.objects.add_bug(**request_data)

            if request_data['push'] == '0':
                # 发送Mind推送
                username = UserInfo.objects.get_user_nick_name(tester)['nick_name']
                mind_uid = UserInfo.objects.get_mind_id(developer_name)['mind_uid']
                notice = f'**{username}** 新建了bug **{request_data["bug_title"]}**  http://test.im30.lan/bug_list/'
                if request_data['png']:
                    for png in request_data['png']:
                        notice = notice + f' ![]({png})'
                robot_message('bug提醒', notice, mind_uid)

            return HttpResponse(json.dumps(data))
            '''
            except:
                data = {
                    "msg": "添加失败"
                }
                return HttpResponse(json.dumps(data))
            '''

    else:
        token = request.COOKIES.get("token", None)
        user_data = jwt.decode(token, "sercet", algorithms=['HS256'])
        username = user_data.get("username", None)
        # todo 修改新增bug逻辑
        project_name = UserInfo.objects.get_project_name(username)[0]

        developer_list = UserInfo.objects.get_develop_user(project_name)
        version_list = Version.objects.get_project_version(project_name)
        module_list = ModuleInfo.objects.get_module_name(project_name)
        project = {
            "project": project_name,
            "developer_list": developer_list,
            "module_list": module_list,
            "version_list": version_list,
        }
        return render(request, 'add_bug.html', context=project)


def edit_bug(request):
    '''
    更改bug状态
    :param request:
    :return:
    '''
    bug_state_data = {'1': '未解决', '2': '已解决', '3': '延期解决', '4': '不解决', '5': '关闭', '6': '激活'}
    if request.is_ajax():
        data = {
            'msg': "更新成功",
            'state': 10000
        }

        request_data = json.loads(request.body.decode('utf-8'))
        bug_id = request_data.get("bug_id")
        if "developer_id" in request_data.keys():
            developer_nick_name = request_data.get("developer_id")
            Bug.objects.update_bug(bug_id=bug_id, developer=developer_nick_name)
        else:
            bug_state = request_data.get("state_" + str(bug_id))
            Bug.objects.update_bug(bug_id=bug_id, bug_state=bug_state)

        bug = Bug.objects.get(id=bug_id)
        bug_state = bug.state
        # 发送Mind推送
        token = request.COOKIES.get("token")
        user_data = jwt.decode(token, "sercet", algorithms=['HS256'])
        operator = user_data.get("username")
        if bug_state == '1' or bug_state == '3' or bug_state == '6':
            user_name = bug.developer

        elif bug_state == '2' or bug_state == '4':
            user_name = bug.buger
        else:
            return HttpResponse(json.dumps(data))
        mind_uid = UserInfo.objects.get_mind_id_by_username(user_name)['mind_uid']
        username = UserInfo.objects.get_user_nick_name(operator)['nick_name']
        notice = f'**{username}** 将bug: **{bug.bug_title}** 置为 **{bug_state_data.get(bug_state)}**  http://test.im30.lan/bug_list/'
        if bug.png != '[]':
            pngs = bug.png.replace('[', '').replace(']', '').replace('\'', '')
            for png in pngs.split(','):
                notice = notice + f' ![]({png})'

        robot_message('bug提醒', notice, mind_uid)

    return HttpResponse(json.dumps(data))

# 遗留bug定时任务


# Create your views here.
from django_apscheduler.jobstores import DjangoJobStore, register_job
from apscheduler.schedulers.background import BackgroundScheduler

from Imoocmapi.models import Bug
from Imoocmapi.utils.common import robot_message

import socket

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 47200))
except:
    print("已启动一个任务计划进程！")
else:
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_jobstore(DjangoJobStore(), "default")


    def legacy_bug_notice_timedtask():
        bug_list = Bug.objects.get_legacy_bug()
        plantform_dict = {}
        developer_dict = {}

        plantform_list = [bug.get('plantform') for bug in bug_list]
        developer_list = [bug.get('developer__nick_name') for bug in bug_list]

        plantform_dict['移动端'] = plantform_list.count('1') + plantform_list.count('2') + plantform_list.count('5')
        plantform_dict['PC端'] = plantform_list.count('3') + plantform_list.count('4')
        plantform_dict['服务端'] = plantform_list.count('6')
        for developer in developer_list:
            developer_dict[developer] = developer_list.count(developer)

        text = '**各端遗留bug如下:**\n'
        for key, value in plantform_dict.items():
            row = f'{key}:{value}\n'
            text = text + row

        text += '**各人遗留bug如下:**\n'
        for key, value in developer_dict.items():
            row = f'{key}:{value}\n'
            text = text + row

        robot_message(name='遗留问题通知', text=str(text), channel='09461611e2b8975afaaa6d2768e5ce42', send_type='group')
        # robot_message(name='遗留问题通知', text=str(text), channel='3903994286', send_type='group')


    scheduler.add_job(legacy_bug_notice_timedtask, trigger='cron', args='', day_of_week='mon-fri',
                      hour=10, minute=0, second=0)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
