# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-10 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0008_auto_20180509_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifyaction',
            old_name='to_user_field',
            new_name='user_list_field',
        ),
        migrations.AddField(
            model_name='notifyaction',
            name='product_parent_table',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
