# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-27 13:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reportview', '0011_auto_20180727_1857'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportprintformataction',
            old_name='parameter',
            new_name='sql',
        ),
    ]