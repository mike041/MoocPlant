# coding=utf-8
import dataclasses
import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import serializers
from ..models import ProjectInfo
from django.forms.models import model_to_dict


class SomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInfo
        fields = "__all__"


def addProject(request):
    '''
    :param request:
    :return:
    '''
    if request.is_ajax():
        response_data = {
            "msg": "添加成功"
        }
        request_data = json.loads(request.body.decode('utf-8'))
        project_name = request_data.get("project_name")
        project_num = ProjectInfo.objects.get_project_num(project_name)
        print(project_num)
        if project_num >= 1:
            response_data['msg'] = "项目已存在"
            return HttpResponse(json.dumps(response_data))
        ProjectInfo.objects.add_project(**request_data)
        return HttpResponse(json.dumps(response_data))
    else:
        return render(request, "add_project.html")


def projectList(request, ajax=False):
    '''
    :param request:
    :return:
    '''

    # projects = ProjectInfo.objects.values("id","project_name")
    # project_data = list([project for project in projects])
    project_data = ProjectInfo.objects.get_project_name_list()

    project_info = {
        "project_info": project_data
    }
    return render(request, "project_list.html", project_info)
