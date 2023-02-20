#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from ..models import Version, ProjectInfo
import json

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
        project_name = request_data.get("project_name")
        version = request_data.get("version")
        version_num = Version.objects.get_project_version_number(project_name=project_name, version=version)
        if version_num > 0:
            data["msg"] = "版本已存在"
            return HttpResponse(json.dumps(data))
        request_data["project_name"] = ProjectInfo.objects.get_project_by_name(project_name)
        Version.objects.add_version(**request_data)
        return HttpResponse(json.dumps(data))
    else:
        project_name_list = ProjectInfo.objects.get_project_name_list()
        project_info = {
            "project_name": project_name_list
        }
        return render(request, "add_version.html",project_info)


def versionList(request):
    '''
    :param request:
    :return:
    '''
    version_list = Version.objects.get_all_version()
    version_info = {
        "version_info":version_list
    }
    return render(request, "version_list.html",version_info)