# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-23 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0013_auto_20180112_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='txtabledetails',
            name='db',
            field=models.CharField(choices=[('server', 'server'), ('client', 'client'), ('both', 'both')], default='server', max_length=50),
            preserve_default=False,
        ),
    ]
