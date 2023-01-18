# Generated by Django 3.2.16 on 2022-10-27 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CpuInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('device_id', models.CharField(max_length=200, verbose_name='手机id')),
                ('use_value', models.FloatField(max_length=10, verbose_name='cpu使用数')),
            ],
            options={
                'verbose_name': 'cpu数据',
                'db_table': 'CpuInfo',
            },
        ),
        migrations.CreateModel(
            name='MemoryInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('device_id', models.CharField(max_length=200, verbose_name='手机id')),
                ('use_value', models.FloatField(max_length=10, verbose_name='Memory使用数')),
            ],
            options={
                'verbose_name': 'Memory数据',
                'db_table': 'MemoryInfo',
            },
        ),
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('project_name', models.CharField(max_length=50, unique=True, verbose_name='项目名称')),
                ('publish_app', models.CharField(max_length=100, verbose_name='发布应用')),
                ('simple_desc', models.CharField(max_length=100, null=True, verbose_name='简要描述')),
            ],
            options={
                'verbose_name': '项目信息',
                'db_table': 'ProjectInfo',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('status', models.IntegerField(default=1, verbose_name='有效/无效')),
            ],
            options={
                'verbose_name': '用户信息',
                'db_table': 'UserInfo',
            },
        ),
        migrations.CreateModel(
            name='ModuleInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('module_name', models.CharField(max_length=50, verbose_name='模块名称')),
                ('simple_desc', models.CharField(max_length=100, null=True, verbose_name='简要描述')),
                ('belong_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Imoocmapi.projectinfo')),
            ],
            options={
                'verbose_name': '模块信息',
                'db_table': 'ModuleInfo',
            },
        ),
    ]
