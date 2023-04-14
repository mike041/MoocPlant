# coding=utf-8
# import xadmin
import xadmin
from xadmin import views
from Imoocmapi.models import UserInfo, ProjectInfo, Version, ModuleInfo, Bug, UserInfoType, UserPermission


class GlobalSettings(object):
    site_title = "学习后台"  # 设置后台左上角标题
    site_footer = "乐学"  # 设置底部页脚


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True  # 这个是打开主题可以切换


class UserAdmin(object):
    # 搜索字段
    search_fields = ['username', 'email','user_type']
    # 显示字段
    list_display = ['id', 'username', 'email', 'status','nick_name','user_type','mind_uid']
    list_editable =['nick_name', 'email', 'user_type','mind_uid']

class UserInfoTypeAdmin(object):
    search_fields = [ 'user_type']
    # 显示字段
    list_display = [ 'id','user_type']

class UserPermissionAdmin(object):
    search_fields =['user_id','system_model','system_url']
    list_display = ['id','user_id','system_model','system_url']
class ProjectAdmin(object):
    search_fields = ['project_name']
    list_display = ['id', 'project_name']


class ModuleAdmin(object):
    search_fields = ['module_name', 'belong_project']
    list_display = ['id', 'module_name', 'belong_project']


class VersionAdmin(object):
    search_fields = ['version']
    list_display = ['id', 'version', 'simple_desc']

class BugAdmin(object):
    search_fields = ['project', 'version','module', 'developer','buger','plantform','state','bug_title']
    list_display = ['project', 'version','module', 'developer','buger','plantform','state','bug_title','push']


xadmin.site.register(UserInfo, UserAdmin)
xadmin.site.register(ProjectInfo, ProjectAdmin)
xadmin.site.register(Version, VersionAdmin)
xadmin.site.register(ModuleInfo, ModuleAdmin)
xadmin.site.register(Bug,BugAdmin)
xadmin.site.register(UserInfoType, UserInfoTypeAdmin)
xadmin.site.register(UserPermission,UserPermissionAdmin)

xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSettings)
