# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smssetup', '0012_delete_editedsmsattributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsattributes',
            name='do',
            field=models.BigIntegerField(default='1'),
            preserve_default=False,
        ),
    ]
