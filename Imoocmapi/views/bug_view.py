# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
import json
from ..models import Bug, ProjectInfo, ModuleInfo

def put_png(request):
    '''
    :param request:
    :return:
    '''
    pass
def bugList(request):
    platformItem = {"1": "IOS", "2": "Android", "3": "web", "4": "pc", "5": "pad"}
    start_level = {'1':'1星','2':'2星','3':'3星','4':'4星'}
    bug_state = {'1':'未解决','2':'已解决','3':'延期解决','4':'不解决','5':'关闭'}
    bug_list = Bug.objects.get_all_bug()
    for bug in bug_list:
        bug['platform'] = platformItem[bug.get("platform")]
        bug['state'] = bug_state[bug.get('state')]
        bug['start'] = start_level[bug.get("start")]
    bug_info = {
        "bug_info": bug_list
    }
    return render(request, 'bug_list.html', bug_info)


def addBug(request):
    if request.is_ajax():
        module_info = {
            "module": None
        }
        request_data = json.loads(request.body.decode('utf-8'))
        project_name = request_data.get("project")
        module_list = ModuleInfo.objects.get_module_name(project_name)
        module_info['module'] = module_list
        return HttpResponse(json.dumps(module_info))
    else:
        project_list = ProjectInfo.objects.get_project_name_list()
        project = {
            "project_list": project_list,
        }
        return render(request, 'add_bug.html', context=project)
