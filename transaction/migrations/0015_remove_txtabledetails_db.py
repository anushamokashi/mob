# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-23 07:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0014_txtabledetails_db'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='txtabledetails',
            name='db',
        ),
    ]
