# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-06 05:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reportview', '0022_reportprintformataction_click_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportprintformataction',
            name='click_event',
        ),
    ]