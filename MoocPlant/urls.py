"""MoocPlant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from Imoocmapi.views import login, index, projectList, addProject, moduleList, addModule, imPerformance, \
    chatPerformance, imChat, envList, addVersion, versionList, addBug, bugList
import xadmin
from MoocPlant import settings

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/assets/img/favicon.ico')),
    path('login/', login),
    path('', index),
    path('project_list/', projectList),
    path('add_project/', addProject),
    path('module_list/', moduleList),
    path('add_module/', addModule),
    path('im_performance/', imPerformance),
    path('chat_performance/', chatPerformance),
    path('im_chat/', imChat),
    path('add_version/', addVersion),
    path('version_list/', versionList),
    path('env_list/', envList),
    path('add_bug/',addBug),
    path('bug_list/',bugList)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
