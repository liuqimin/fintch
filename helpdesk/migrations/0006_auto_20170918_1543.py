# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0005_auto_20170918_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='macaddress',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True, verbose_name='MAC地址'),
        ),
    ]