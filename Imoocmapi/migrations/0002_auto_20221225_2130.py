# Generated by Django 3.2.16 on 2022-12-25 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Imoocmapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('start', models.CharField(choices=[('1', '1星'), ('2', '2星'), ('3', '3星'), ('4', '4星')], max_length=12, verbose_name='几星')),
                ('bug_title', models.CharField(max_length=500, verbose_name='bug描述')),
                ('bug_content', models.CharField(max_length=1000, verbose_name='bug详情')),
                ('platform', models.CharField(choices=[('1', 'ios'), ('2', 'android'), ('3', 'web'), ('4', 'pc'), ('5', 'pad')], max_length=12, verbose_name='bug所属平台')),
                ('state', models.CharField(choices=[('1', '未解决'), ('2', '已解决'), ('3', '延期解决'), ('4', '不解决'), ('5', '关闭')], max_length=12, verbose_name='bug状态')),
                ('pic', models.ImageField(blank=True, upload_to='images/bug', verbose_name='bug图片')),
                ('push', models.BooleanField(choices=False, verbose_name='是否推送')),
            ],
            options={
                'verbose_name': 'bug',
                'db_table': 'Bug',
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('version', models.CharField(max_length=20, verbose_name='版本号')),
            ],
            options={
                'verbose_name': '版本信息',
                'db_table': 'Version',
            },
        ),
        migrations.DeleteModel(
            name='CpuInfo',
        ),
        migrations.DeleteModel(
            name='MemoryInfo',
        ),
        migrations.RemoveField(
            model_name='projectinfo',
            name='publish_app',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='status',
            field=models.IntegerField(default=1, verbose_name='用户状态'),
        ),
        migrations.AddField(
            model_name='bug',
            name='buger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buger', to='Imoocmapi.userinfo', verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='bug',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='developer', to='Imoocmapi.userinfo', verbose_name='开发人员'),
        ),
        migrations.AddField(
            model_name='bug',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Imoocmapi.moduleinfo', verbose_name='模块'),
        ),
        migrations.AddField(
            model_name='bug',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Imoocmapi.projectinfo', verbose_name='项目'),
        ),
        migrations.AddField(
            model_name='bug',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Imoocmapi.version', verbose_name='版本'),
        ),
        migrations.AddField(
            model_name='projectinfo',
            name='version',
            field=models.ForeignKey(default=1.0, on_delete=django.db.models.deletion.CASCADE, to='Imoocmapi.version', verbose_name='版本'),
            preserve_default=False,
        ),
    ]
