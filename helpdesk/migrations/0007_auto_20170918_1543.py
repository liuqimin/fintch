# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 07:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0006_auto_20170918_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='ipaddress',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='macaddress',
        ),
    ]
