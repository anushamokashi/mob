# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-24 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20180110_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='ionicservices',
            name='context',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='ionicservices',
            name='host',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='ionicservices',
            name='port',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='ionicservices',
            name='protocol',
            field=models.CharField(choices=[('http://', 'HTTP'), ('https://', 'HTTPS')], default='http://', max_length=50),
            preserve_default=False,
        ),
    ]
