# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-18 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0014_auto_20180717_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='txnprintformataction',
            name='JasperFile',
            field=models.FileField(upload_to='static/ionicmeta/%Y/%m/%d'),
        ),
    ]
