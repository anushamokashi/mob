# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-06 05:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printformat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printformat',
            name='iconcls',
        ),
    ]
