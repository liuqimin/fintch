# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 02:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32, verbose_name='服务器名')),
                ('ext_ip', models.GenericIPAddressField()),
                ('int_ip', models.GenericIPAddressField()),
                ('status', models.IntegerField(choices=[(1, '使用'), (2, '未使用'), (3, '下线')])),
            ],
            options={
                'verbose_name': '基础表',
                'verbose_name_plural': '基础表',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('url_type', models.SmallIntegerField(choices=[(0, 'relative_name'), (1, 'absolute_url')])),
                ('url_name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proyecto', models.CharField(max_length=32, verbose_name='项目名')),
                ('servidor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Base')),
            ],
            options={
                'verbose_name': '项目表',
                'verbose_name_plural': '项目表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('menus', models.ManyToManyField(to='base.Menu')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=32, verbose_name='服务名')),
                ('entorno', models.CharField(choices=[('uat', '测试环境'), ('prd', '生产环节'), ('demo', '演示环境')], max_length=8, verbose_name='环境')),
                ('port', models.IntegerField(verbose_name='端口')),
                ('jar', models.CharField(blank=True, max_length=32, null=True, verbose_name='java包名')),
                ('jar_load', models.CharField(blank=True, max_length=32, null=True, verbose_name='java包名')),
                ('servidor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Base')),
            ],
            options={
                'verbose_name': '服务表',
                'verbose_name_plural': '服务表',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('roles', models.ManyToManyField(blank=True, null=True, to='base.Role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
