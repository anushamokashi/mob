# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-28 05:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_emailconfiguration_db_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='table_append_by_underscore',
            field=models.BooleanField(default=False),
        ),
    ]
