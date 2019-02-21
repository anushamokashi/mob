# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-31 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0012_auto_20180530_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actions',
            name='actiontype',
            field=models.CharField(blank=True, choices=[('cancel', 'Cancel'), ('delete', 'Delete'), ('new', 'New'), ('save', 'Save'), ('search', 'Search')], max_length=50, null=True),
        ),
    ]
