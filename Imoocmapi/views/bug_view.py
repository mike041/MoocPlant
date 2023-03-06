# coding=utf-8
import jwt
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import json

from .user_view import check_login
from ..models import Bug, ProjectInfo, ModuleInfo, Version, UserInfo
from ..utils.tencent_cos import TencentCOS
import os
import datetime


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
        # 将原始文件名作为key传给COS
        key = 'mooc plant/' + file_full_name
        # 调用COS上传文件，返回url
        upload = TencentCOS().upload_cos(local_file, key)
        file_list = [upload]
        return HttpResponse(json.dumps({'success': 1,
                                        'message': "上传成功！",
                                        'data': file_list
                                        }))


@check_login
def bugList(request):
    platformItem = {"1": "IOS", "2": "Android", "3": "web", "4": "pc", "5": "pad","6":"服务端"}
    start_level = {'1': '1星', '2': '2星', '3': '3星', '4': '4星'}
    bug_state = {'1': '未解决', '2': '已解决', '3': '延期解决', '4': '不解决', '5': '关闭', '6': '激活'}
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        token = request.COOKIES.get("token", None)
        user_data = jwt.decode(token, "sercet", algorithms=['HS256'])
        user_type = user_data.get("user_type", None)
        username = user_data.get("username", None)
        if "only_me" in data.keys():
            if user_type == 3:
                data["buger"] = username
            else:
                data["developer"] = username
        bug_list = Bug.objects.search_bug(**data)
    else:
        bug_list = Bug.objects.get_all_bug()

    project_list = []
    for bug in bug_list:
        bug_png_list = []
        bug['plantform'] = platformItem[bug.get("plantform")]
        bug['state'] = bug_state[bug.get('state')]
        bug['start'] = start_level[bug.get("start")]
        bug_png = bug['png']
        if bug_png is not None and bug_png != "":
            if "," in bug_png:
                bug_png_list = eval(bug_png)
            else:
                bug_png_list.append(bug_png)

            bug['png'] = bug_png_list
            bug['png_size'] = 60 * len(bug_png_list)
        if bug["project__project_name"] not in project_list:
            project_list.append(bug["project__project_name"])

    bug_info = {
        "bug_info": bug_list,
        "project_list": project_list
    }
    if request.is_ajax():
        return HttpResponse(json.dumps(bug_info))
    else:
        return render(request, 'bug_list.html', bug_info)



@check_login
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
            return HttpResponse(json.dumps(module_info))
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
            return HttpResponse(json.dumps(data))
            '''
            except:
                data = {
                    "msg": "添加失败"
                }
                return HttpResponse(json.dumps(data))
            '''

    else:
        project_list = ProjectInfo.objects.get_project_name_list()
        developer_list = UserInfo.objects.get_develop_user()
        project = {
            "project_list": project_list,
            "developer_list": developer_list
        }
        return render(request, 'add_bug.html', context=project)


def edit_bug(request):
    '''
    更改bug状态
    :param request:
    :return:
    '''
    if request.is_ajax():
        data = {
            'msg': "更新成功",
            'state': 10000
        }

        request_data = json.loads(request.body.decode('utf-8'))
        bug_id = request_data.get("bug_id")
        bug_state = request_data.get("state")
        Bug.objects.update_bug(bug_id, bug_state)
        return HttpResponse(json.dumps(data))
