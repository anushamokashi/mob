# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-14 11:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smssetup', '0009_smsserver_use_proxy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editedsmsattributes',
            name='old_key',
        ),
        migrations.RemoveField(
            model_name='editedsmsattributes',
            name='smsattr_id',
        ),
    ]