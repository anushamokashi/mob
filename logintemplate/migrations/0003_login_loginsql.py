# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-05 11:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logintemplate', '0002_auto_20180716_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='loginsql',
            field=models.CharField(default='sql', max_length=550),
            preserve_default=False,
        ),
    ]
