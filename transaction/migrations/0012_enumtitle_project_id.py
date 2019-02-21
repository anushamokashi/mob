# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-12 05:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20180110_1527'),
        ('transaction', '0011_auto_20180111_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='enumtitle',
            name='project_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
            preserve_default=False,
        ),
    ]
