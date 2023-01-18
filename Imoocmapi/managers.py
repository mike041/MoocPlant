# -*- encoding: utf-8 -*-
"""
@File    :   managers.py
@Time    :   2022/10/22 17:34
@Author  :   Mushishi 
"""
from django.db import models


class UserInfoManager(models.Manager):
    """
    用户信息表操作自定义管理器
    """

    def register_user(self, username, password, email):
        """
        用户注册
        :param username:
        :param password:
        :param email:
        :return:
        """
        self.create(username=username, password=password, email=email)

    def get_user(self, username, password):
        """
        用户登录，获取登录
        :param username:
        :param password:
        :return:
        """
        return self.filter(username__exact=username, password__exact=password).count()


class ProjectInfoManager(models.Manager):
    """
    项目信息表操作自定义管理器
    """

    def add_project(self, **kwargs):
        """
        添加项目
        :param kwargs:
        :return:
        """
        self.create(**kwargs)

    def get_project(self, project_id):
        return self.get(id=project_id)

    def update_project(self, project_id, **kwargs):
        """
        更新项目信息
        :param project_id:
        :param kwargs:
        :return:
        """
        project_info = self.get(id=project_id)
        project_info.project_name = kwargs.get("project_name")
        project_info.publish_app = kwargs.get("publish_app")
        project_info.simple_desc = kwargs.get("simple_desc")
        project_info.save()

    def get_project_num(self, project_name, project_id=None):
        """
        获取项目数
        :param project_name:
        :param project_id:
        :return:
        """
        return self.filter(project_name__exact=project_name).count()

    def get_project_name_list(self):
        '''
        获取所有项目名字
        :return:
        '''
        projects = self.values("id", "project_name", "simple_desc", "create_time")
        project_data = list([project for project in projects])
        return project_data


class ModuleInfoManager(models.Manager):
    """
    项目模块信息表 自定义管理器
    """

    def add_module(self, **kwargs):
        # self.get_or_create()
        self.create(**kwargs)

    def get_module_name(self, project_name):
        module_list = self.filter(belong_project__project_name=project_name).values("module_name")
        module_name_list = [module for module in module_list]
        return module_name_list

    def get_all_module_name(self):
        module_list = self.all().values("module_name", "belong_project__project_name", "create_time")
        module_name_list = [module for module in module_list]
        return module_name_list  # 62355068


class VersionManager(models.Manager):
    '''
    版本管理
    '''
    def add_version(self,**kwargs):
        self.create(**kwargs)

    def get_all_version(self):
        version_list = self.values("id", "version", "project_name__project_name", "simple_desc", "create_time")
        version_name_list = [version for version in version_list]
        return version_name_list  # 62355068


class BugManager(models.Manager):
    '''
    bug管理
    '''
    def add_bug(self,**kwargs):
        self.create(**kwargs)

    def get_all_bug(self):
        '''
        展示所有bug
        :return:
        '''
        bug_list = list(self.values("id","project__project_name","module__module_name","version__version","bug_title","platform","state","start","developer__username"))
        #self.values("id","project__")
        return bug_list

class TestCaseSuiteInfoManager(models.Manager):
    """
    测试套件信息表 自定义管理器
    """
    pass


class EnvInfoManager(models.Manager):
    """
    环境信息表 自定义管理器
    """
    pass


class TestCaseInfoManager(models.Manager):
    """
    测试case表 自定义管理器
    """
    pass
