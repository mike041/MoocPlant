from dataclasses import dataclass

from django.db import models

from Imoocmapi.managers import ProjectInfoManager, ModuleInfoManager, VersionManager, BugManager, UserInfoManager


class BaseTable(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'


class UserInfoType(BaseTable):
    class Meta:
        verbose_name = '用户类型'
        db_table = "UserInfoType"

    user_type = models.CharField(verbose_name='用户类型名字', max_length=10)

    def __str__(self):
        return self.user_type


class ProjectInfo(BaseTable):
    class Meta:
        verbose_name = '项目信息'
        db_table = 'ProjectInfo'

    project_name = models.CharField('项目名称', max_length=50, unique=True, null=False)
    # version = models.ForeignKey(Version, verbose_name='版本', on_delete=models.CASCADE, default="1.0")
    simple_desc = models.CharField('简要描述', max_length=100, null=True)
    objects = ProjectInfoManager()

    def __str__(self):
        return self.project_name


class UserGroup(BaseTable):
    class Meta:
        verbose_name = '用户组'
        db_table = 'UserGroup'

    group_name = models.CharField(verbose_name='用户组名', max_length=20)

    def __str__(self):
        return self.group_name


class UserInfo(BaseTable):
    class Meta:
        verbose_name = '用户信息'
        db_table = 'UserInfo'

    username = models.CharField(verbose_name='用户名', max_length=20, unique=True, null=False)
    password = models.CharField(verbose_name='密码', max_length=20, null=False)
    nick_name = models.CharField(verbose_name="昵称", max_length=20, unique=True, default='test')
    email = models.EmailField(verbose_name='邮箱', null=False, unique=True)
    status = models.IntegerField(verbose_name='用户状态', default=1)
    user_type = models.ForeignKey(UserInfoType, on_delete=models.CASCADE, max_length=10, default=2)
    mind_uid = models.CharField(verbose_name='mind用户id', max_length=50, null=True, blank=True)
    project_name = models.ForeignKey(ProjectInfo, verbose_name="项目", on_delete=models.CASCADE, null=True)
    objects = UserInfoManager()

    def __str__(self):
        return self.username


class UserPermission(BaseTable):
    class Meta:
        verbose_name = '用户权限表'
        db_table = 'UserPermission'

    user_id = models.ForeignKey(UserInfo, verbose_name="用户id", on_delete=models.CASCADE)
    system_model = models.CharField(verbose_name='系统功能模块名', max_length=50)


class EnvInfo(BaseTable):
    class Meta:
        verbose_name = '环境管理'
        db_table = 'EnvInfo'

    env_name = models.CharField(max_length=40, null=False, unique=True)
    http_url = models.CharField(max_length=40, verbose_name="http url", null=False)
    ws_url = models.CharField(max_length=40, verbose_name="websocket url", null=False)
    conversationId = models.CharField(max_length=50, verbose_name="话题id", null=False)
    groupId = models.CharField(max_length=50, verbose_name="组id", null=False)
    testPhone = models.TextField(max_length=10000, verbose_name="测试账号", null=False)
    simple_desc = models.CharField(max_length=50, null=False)


class Version(BaseTable):
    class Meta:
        verbose_name = '版本信息'
        db_table = 'Version'

    version = models.CharField(verbose_name='版本号', max_length=20)
    project_name = models.ForeignKey(ProjectInfo, verbose_name="项目", on_delete=models.CASCADE, null=True)
    simple_desc = models.CharField(max_length=50, verbose_name="版本描述信息", null=True)
    objects = VersionManager()

    def __str__(self):
        return self.version


class ModuleInfo(BaseTable):
    class Meta:
        verbose_name = '模块信息'
        db_table = 'ModuleInfo'

    module_name = models.CharField('模块名称', max_length=50, null=False)
    belong_project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    simple_desc = models.CharField('简要描述', max_length=100, null=True)

    objects = ModuleInfoManager()

    def __str__(self):
        return self.module_name


class Bug(BaseTable):
    start_level = (
        ('1', '1星'),
        ('2', '2星'),
        ('3', '3星'),
        ('4', '4星')
    )
    platform_choices = (
        ('1', 'ios'),
        ('2', 'android'),
        ('3', 'web'),
        ('4', 'pc'),
        ('5', 'pad'),
        ('6', '服务端'),
    )
    bug_state = (
        ('1', '未解决'),
        ('2', '已解决'),
        ('3', '延期解决'),
        ('4', '不解决'),
        ('5', '关闭'),
        ('6', '激活'),

    )
    choices_push = (
        (False, '推送'),
        (True, '不推送')
    )

    class Meta:
        verbose_name = 'bug'
        db_table = "Bug"

    project = models.ForeignKey(ProjectInfo, verbose_name="项目", on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleInfo, verbose_name='模块', on_delete=models.CASCADE)
    version = models.ForeignKey(Version, verbose_name="版本", on_delete=models.CASCADE)
    developer = models.ForeignKey(UserInfo, verbose_name="开发人员", related_name='developer', on_delete=models.CASCADE)
    start = models.CharField(verbose_name="几星", choices=start_level, max_length=12)
    buger = models.ForeignKey(UserInfo, verbose_name="创建者", related_name="buger", on_delete=models.CASCADE)
    bug_title = models.CharField(verbose_name="bug描述", max_length=500)
    bug_content = models.CharField(verbose_name="bug详情", max_length=1000)
    plantform = models.CharField(verbose_name="bug所属平台", choices=platform_choices, max_length=12)
    state = models.CharField(verbose_name="bug状态", choices=bug_state, max_length=12)
    pic = models.ImageField(verbose_name="bug图片", upload_to="images/bug", blank=True)
    png = models.CharField(verbose_name="图片地址", max_length=500, null=True)
    push = models.BooleanField(verbose_name="是否推送", choices=choices_push)
    objects = BugManager()

    def __str__(self):
        return self.bug_title
