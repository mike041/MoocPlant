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
from Imoocmapi.views import base_view, bug_view, module_view, project_view, user_view, version_view, user_view, \
    interface_view
import xadmin
from MoocPlant import settings

urlpatterns = [
                  path('xadmin/', xadmin.site.urls),
                  re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/assets/img/favicon.ico')),
                  path('login/', user_view.login),
                  path('', user_view.index),
                  path('index/', user_view.index),
                  path('project_list/', project_view.projectList),
                  path('add_project/', project_view.addProject),
                  path('module_list/', module_view.moduleList),
                  path('add_module/', module_view.addModule),
                  path('im_performance/', base_view.imPerformance),
                  path('chat_performance/', base_view.chatPerformance),
                  path('interface_performance/',base_view.interfacePerformance),
                  path('im_chat/', base_view.imChat),
                  path('add_version/', version_view.addVersion),
                  path('version_list/', version_view.versionList),
                  path('env_list/', base_view.envList),
                  path('add_bug/', bug_view.addBug),
                  path('bug_list/', bug_view.bugList),
                  path('put_png/', bug_view.put_png),
                  path('edit_bug/', bug_view.edit_bug),
                  path("log_out/", user_view.logout),
                  path("interface_list/", interface_view.interface_list),
                  path("add_interface/", interface_view.add_interface),
                  path('develop_list/', user_view.get_developer),
                  path('no_auth/', user_view.no_auth)

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
