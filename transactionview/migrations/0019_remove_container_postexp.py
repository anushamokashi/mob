# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-24 05:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactionview', '0018_transactionview_expression'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='postexp',
        ),
    ]
