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


class ModuleInfoManager(models.Manager):
    """
    项目模块信息表 自定义管理器
    """
    pass


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

