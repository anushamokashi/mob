# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-08 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0016_auto_20180124_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='txtablecomponentdetails',
            name='db_type',
            field=models.CharField(choices=[('server', 'server'), ('client', 'client'), ('both', 'both')], default='both', max_length=50),
        ),
        migrations.AddField(
            model_name='txtabledetails',
            name='db_type',
            field=models.CharField(choices=[('server', 'server'), ('client', 'client'), ('both', 'both')], default='both', max_length=50),
        ),
    ]
