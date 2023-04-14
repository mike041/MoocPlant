# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render

from .user_view import check_login, chech_user_auth
from ..models import Version, ProjectInfo
import json


@check_login
@chech_user_auth
def addVersion(request):
    '''
    :param request:
    :return:
    '''
    if request.is_ajax():
        data = {
            "msg": "成功"
        }
        request_data = json.loads(request.body.decode('utf-8'))
        project_name = request_data.get('project_name')
        version = request_data.get('version')
        version_number = Version.objects.get_version_by_project_name(project_name, version)
        if version_number >= 1:
            data["msg"] = "版本号已存在"
            return HttpResponse(json.dumps(data))
        project_name = ProjectInfo.objects.get_project_by_name(project_name)
        request_data["project_name"] = project_name
        Version.objects.add_version(**request_data)
        return HttpResponse(json.dumps(data))
    else:
        project_name_list = ProjectInfo.objects.get_project_name_list()
        project_info = {
            "project_name": project_name_list
        }
        return render(request, "add_version.html", project_info)


@check_login
@chech_user_auth
def versionList(request):
    '''
    :param request:
    :return:
    '''
    if request.is_ajax():
        data = {
            "msg": "成功",
            "versions": None
        }
        request_data = json.loads(request.body.decode('utf-8'))
        project_name = request_data.get('project')
        version_list = Version.objects.get_project_version(project_name)
        data["versions"] = version_list
        return HttpResponse(json.dumps(data))
    else:
        version_list = Version.objects.get_all_version()
        version_info = {
            "version_info": version_list
        }
        return render(request, "version_list.html", version_info)


