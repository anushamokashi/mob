# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-27 13:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reportview', '0010_auto_20180725_1515'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportprintformataction',
            old_name='JasperFile',
            new_name='htmlfile',
        ),
    ]
