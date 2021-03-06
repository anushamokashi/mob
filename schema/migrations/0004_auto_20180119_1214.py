# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-19 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0003_auto_20180112_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_connections_info',
            name='dbname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='db_connections_info',
            name='host',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='db_connections_info',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='db_connections_info',
            name='port',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='db_connections_info',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
