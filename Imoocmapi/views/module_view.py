# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render

from Imoocmapi.models import ModuleInfo, ProjectInfo
import json

from Imoocmapi.views.base_view import check_login


def addModule(request):
    '''
    :param request:
    :return:
    '''
    if request.is_ajax():
        data = {
            "msg": "成功"
        }
        request_data = json.loads(request.body.decode('utf-8'))
        project_name = request_data.get("belong_project")
        module_name = request_data.get("module_name")
        module_num = ModuleInfo.objects.get_module_num(project_name, module_name)
        if module_num >= 1:
            data['msg'] = "模块已存在"
            return HttpResponse(json.dumps(data))
        belong_project = ProjectInfo.objects.get_project(project_id=request_data.get("belong_project"))
        request_data["belong_project"] = belong_project
        ModuleInfo.objects.add_module(**request_data)
        return HttpResponse(json.dumps(data))
    else:
        project_name_list = ProjectInfo.objects.get_project_name_list()
        project_info = {
            "project_name": project_name_list
        }
        return render(request, "add_module.html", project_info)


@check_login
def moduleList(request):
    '''
    :param ajax:
    :param request:
    :return:
    '''
    #
    module_info = {
        "module": None
    }
    if request.is_ajax():
        request_data = json.loads(request.body.decode('utf-8'))
        project_name = request_data.get("project")
        module_list = ModuleInfo.objects.get_module_name(project_name)
        module_info['module'] = module_list
        return HttpResponse(json.dumps(module_info))
    else:
        module_list = ModuleInfo.objects.get_all_module_name()
        module_info['module'] = module_list
        print(module_info)
        return render(request, "module_list.html", module_info)
