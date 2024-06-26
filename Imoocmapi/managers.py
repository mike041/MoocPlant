# -*- encoding: utf-8 -*-
"""
@File    :   managers.py
@Time    :   2022/10/22 17:34
@Author  :   Mushishi 
"""
from django.db import models
from django.db.models import Q


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

    def get_user_count(self, username, password):
        """
        用户登录，获取登录
        :param username:
        :param password:
        :return:
        """
        return self.filter(username=username, password=password).count()

    def get_develop_user(self, project_name):
        '''
        获取所有开发人员
        :return:
        '''
        nick_name_list = self.filter(user_type=2, project_name__project_name=project_name).values("id", "nick_name")
        nick_name_data = list([nick_name for nick_name in nick_name_list])
        return nick_name_data

    def get_user_by_user_name(self, user_name=None, nick_name=None):
        if user_name is None:
            return self.get(nick_name=nick_name)
        else:
            return self.get(username=user_name)

    def get_user_nick_name(self, user_name):
        result = self.filter(username=user_name).values("nick_name", "user_type").first()
        return result

    def get_mind_id(self, user_name):
        '''
        根据用户名获取mind uid
        :param user_name:
        :return:
        '''
        result = self.filter(nick_name=user_name).values("mind_uid").first()
        return result

    def get_mind_id_by_username(self, user_name):
        '''
        根据username获取mind uid
        :param user_name:
        :return:
        '''
        result = self.filter(username=user_name).values("mind_uid").first()
        return result

    def get_project_name(self, user_name):
        '''
        根据username获取project_name
        :param user_name:
        :return:
        '''
        project_name = list([project.get("project_name__project_name") for project in
                             self.filter(username=user_name).values("project_name__project_name")])
        # project_name = self.get(username=user_name).project_name
        return project_name


class UserPermissionManager(models.Manager):
    """
    用户权限自定义管理器
    """

    def get_user_permission(self, username):
        '''
        获取用户权限
        :return:
        '''
        system_url_list = self.filter(user_id__username=username).values("system_url")
        url_data = list([system_url for system_url in system_url_list])
        return url_data


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

    def get_project_by_name(self, project_name):
        return self.get(project_name=project_name)

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

    def get_project_num(self, project_name):
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

    def get_module(self, project_name, module_name):
        return self.filter(Q(belong_project__project_name=project_name) & Q(module_name=module_name)).first()

    def get_module_name(self, project_name):
        module_list = self.filter(belong_project__project_name=project_name).values("module_name")
        module_name_list = [module for module in module_list]
        return module_name_list

    def get_all_module_name(self):
        module_list = self.all().values("module_name", "belong_project__project_name", "create_time")
        module_name_list = [module for module in module_list]
        return module_name_list  # 62355068

    def get_module_num(self, project_name, module_name):
        return self.filter(Q(belong_project=project_name) & Q(module_name=module_name)).count()


class VersionManager(models.Manager):
    '''
    版本管理
    '''

    def add_version(self, **kwargs):
        self.create(**kwargs)

    def get_project_version(self, project_name):
        version_list = self.filter(Q(project_name__project_name=project_name)).values("version").order_by("-id")[0:10]
        online_list = self.filter(Q(project_name__project_name=project_name) & Q(version__contains="线上")).values(
            "version")
        approval = self.filter(Q(project_name__project_name=project_name) & Q(version__contains="审批商业化")).values(
            "version")
        multi_tenancy = self.filter(Q(project_name__project_name=project_name) & Q(version__contains="多租户")).values(
            "version")
        version_name_list = [version for version in version_list]
        online_version_name_list = [version for version in online_list]
        version_name_list.extend(online_version_name_list)
        version_name_list.extend(approval)
        version_name_list.extend(multi_tenancy)
        return version_name_list

    def get_all_version(self):
        version_list = self.values("id", "version", "project_name__project_name", "simple_desc", "create_time")
        version_name_list = [version for version in version_list]
        return version_name_list  # 62355068

    def get_version(self, project_name, version):
        return self.get(Q(project_name__project_name=project_name) & Q(version=version))

    def get_version_by_project_name(self, project_name, version):
        '''
        想过项目名字、versio获取该项目该版本是否存在
        :param project_name:
        :param version:
        :return:
        '''
        return self.filter(Q(project_name__project_name=project_name) & Q(version=version)).count()


class BugManager(models.Manager):
    '''
    bug管理
    '''

    def add_bug(self, **kwargs):
        self.create(**kwargs)

    def get_all_bug(self, project_name):
        '''
        展示所有bug
        :return:
        '''
        bug_list_object = self.filter(~Q(state=5) & (Q(project__project_name__in=project_name)))
        # bug_list.values()
        bug_list = list(bug_list_object.values("id", "project__project_name", "module__module_name", "version__version",
                                               "bug_title",
                                               "plantform", "state", "start", "developer__nick_name",
                                               "buger__nick_name", "png").order_by("-id"))
        # self.values())
        # self.values("id","project__")

        return bug_list

    def get_legacy_bug(self):
        '''
        获取遗留的所有bug,只针对mind项目
        :return:
        '''
        bug_list_object = self.filter(
            (Q(state=1) | Q(state=3) | Q(state=6)) & (Q(project=1)))
        # bug_list.values()
        bug_list = list(bug_list_object.values("id", "project__project_name", "module__module_name", "version__version",
                                               "bug_title",
                                               "plantform", "state", "start", "developer__nick_name",
                                               "buger__nick_name", "png").order_by("-id"))
        # self.values())
        # self.values("id","project__")

        return bug_list

    def update_bug(self, bug_id, bug_state=None, developer=None):
        '''
        更新bug
        :param bug_id:
        :return:
        '''
        bug = self.filter(id=bug_id)
        if bug_state is not None:
            bug.update(state=bug_state)
        else:
            bug.update(developer=int(developer))

    def search_bug1(self, args):
        print(args)
        bug_version = args.get("search_versions")
        args.pop("search_versions")

        if "buger" in args.keys():
            buger = args.get("buger")
            args.pop("buger")
        # {'project': 'All', 'module': 'All', 'developer': '', 'search_versions': 'All', 'only_me': '0'}
        project_name, module_name, developer_name, bug_version, only_me = args.values()

        if project_name == 'All':
            self.filter()

    def search_bug(self, args):
        """
        根据项目、模块查找bug
        :param args:
        :return:
        """
        # self.filter(**args)
        print(args)
        bug_version = args.get("search_versions")
        buger = args.get("buger", None)
        if buger is not None:
            args.pop("buger")
        args.pop("search_versions")
        title = args.pop("title")
        project_name, module_name, version, platform, status, developer_name, only_me = args.values()

        query = Q(project__project_name__in=project_name) & ~Q(state=5)

        if module_name != "All":
            query = query & Q(module__module_name=module_name)
        if version != "All":
            query = query & Q(version__version=version)
        if platform != "All":
            query = query & Q(plantform=platform)
        if status != "All":
            query = query & Q(state=status)
        if developer_name != '':
            query = query & Q(developer__nick_name=developer_name)
        if buger is not None:
            query = (query & Q(buger__username=buger)) | query & Q(developer__username=buger)

        # if module_name == "All":
        #     if developer_name != "":
        #         if only_me == "1" and buger is not None:
        #             query = Q(project__project_name__in=project_name) & Q(buger__username=buger) & Q(
        #                 developer__nick_name=developer_name) & ~Q(state=5)
        #         else:
        #             query = Q(project__project_name__in=project_name) & Q(developer__nick_name=developer_name) & ~Q(
        #                 state=5)
        #
        #     else:
        #         if only_me == "1" and buger is not None:
        #             query = Q(project__project_name__in=project_name) & Q(buger__username=buger) & ~Q(state=5)
        #         else:
        #             query = Q(project__project_name__in=project_name) & ~Q(state=5)
        # else:
        #     query = Q(project__project_name__in=project_name) & Q(module__module_name=module_name) & ~Q(state=5)

        '''
        if "buger" in args.keys():
            buger = args.get("buger")
            args.pop("buger")
        #{'project': 'All', 'module': 'All', 'developer': '', 'search_versions': 'All', 'only_me': '0'}
        project_name, module_name, developer_name, bug_version, only_me = args.values()
        
        if project_name == 'All':
            self.filter()
        '''
        '''
        if "buger" in args.keys() and "only_me" in args.keys():
            if bug_version == "All":
                bug_version = 99
                bug_list = self.filter(
                    Q(buger__username=args["buger"]) & ~Q(version__version=bug_version) & ~Q(state=5))
            else:
                bug_list = self.filter(Q(buger__username=args["buger"]) & Q(version__version=bug_version) & ~Q(state=5))
        if "only_me" in args.keys() and "buger" not in args.keys():
            if bug_version != "All":
                bug_list = self.filter(
                    Q(developer__username=args["developer"]) & Q(version__version=bug_version) & ~Q(state=5))
            else:
                bug_version = 99
                bug_list = self.filter(
                    Q(developer__username=args["developer"]) & ~Q(version__version=bug_version) & ~Q(state=5))
        if "only_me" not in args.keys():
            project_name, module_name, developer_name, only_me = args.values()
            print("--->>>>>>>>",args)
            if module_name == "All":
                bug_list = self.filter(Q(module__module_name=module_name) & Q(project__project_name__in=project_name))
                print("--->>>",bug_list)
            if project_name != "All":
                if module_name != "" and developer_name != "" and module_name != "All" and developer_name != "All":
                    if bug_version != "All":
                        bug_list = self.filter(
                            Q(project__project_name=project_name) & Q(module__module_name=module_name) & Q(
                                version=bug_version) & ~Q(state=5))
                    else:
                        bug_version = 99
                        bug_list = self.filter(
                            Q(project__project_name=project_name) & Q(module__module_name=module_name) & ~Q(
                                version=bug_version) & ~Q(state=5))
                elif module_name != "All" and developer_name == "":
                    if bug_version != "All":
                        bug_list = self.filter(
                            Q(project__project_name=project_name) & Q(module__module_name=module_name) & Q(
                                version=bug_version) & ~Q(state=5))
                    else:
                        bug_version = 99
                        bug_list = self.filter(
                            Q(project__project_name=project_name) & Q(module__module_name=module_name) & ~Q(
                                version=bug_version) & ~Q(state=5))
                elif module_name == "All" and developer_name == "":
                    if bug_version != "All":
                        bug_list = self.filter(
                            Q(project__project_name=project_name) & Q(version__version=bug_version) & ~Q(state=5))
                    else:
                        bug_version = 99
                        bug_list = self.filter(
                            Q(project__project_name=project_name) & ~Q(version=bug_version) & ~Q(state=5))
                elif module_name == "All" and developer_name != "":
                    if bug_version != "All":
                        bug_list = self.filter(
                            Q(project__project_name=project_name) & Q(developer__nick_name=developer_name) & Q(
                                version__version=bug_version) & ~Q(state=5))
                    else:
                        bug_version = 99
                        bug_list = self.filter(
                            Q(project__project_name=project_name) & Q(developer__nick_name=developer_name) & ~Q(
                                version=bug_version) & ~Q(state=5))
            else:
                if developer_name != "" and project_name == "All":
                    bug_list = self.filter(developer__nick_name=developer_name)
                else:
                    print("----------->")
                    bug_list = self.filter(~Q(state=5))
        '''

        if title != '':
            query = query & Q(bug_title__icontains=title)

        bug_list = self.filter(query)

        return list(
            bug_list.values("id", "project__project_name", "module__module_name", "version__version", "bug_title",
                            "plantform", "state", "start", "developer__nick_name", "buger__nick_name", "png").order_by(
                "-id"))

    def bug_statistics(self, args):
        # todo 还未按照版本区分，查询的是所有的版本的未关闭的bug

        username, user_type, project_name, statistics = args.values()
        # 开发
        if user_type == 2:
            if statistics == 1:
                bug_list = self.filter(Q(developer__username=username) & Q(project__project_name__in=project_name)
                                       & Q(Q(state=1) | Q(state=3) | Q(state=6)))
                bug_list = self.filter(Q(developer__username=username) & Q(project__project_name__in=project_name))
            elif statistics == 2:
                bug_list = self.filter(Q(developer__username=username) & Q(project__project_name__in=project_name)
                                       & Q(Q(state=1) | Q(state=3) | Q(state=6)))
            elif statistics == 3:
                bug_list = self.filter(Q(developer__username=username) & Q(project__project_name__in=project_name) & Q(
                    Q(state=2) | Q(state=4)))
        else:  # 测试或产品
            if statistics == 1:
                bug_list = self.filter(Q(buger__username=username) & Q(project__project_name__in=project_name)
                                       & Q(Q(state=1) | Q(state=3) | Q(state=6)))
            elif statistics == 2:
                bug_list = self.filter(Q(buger__username=username) & Q(project__project_name__in=project_name)
                                       & Q(Q(state=1) | Q(state=3) | Q(state=6)))
            elif statistics == 3:
                bug_list = self.filter(Q(buger__username=username) & Q(project__project_name__in=project_name) & Q(
                    Q(state=2) | Q(state=4)))
        return list(
            bug_list.values("id", "project__project_name", "module__module_name", "version__version", "bug_title",
                            "plantform", "state", "start", "developer__nick_name", "buger__nick_name", "png").order_by(
                "-id"))


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
