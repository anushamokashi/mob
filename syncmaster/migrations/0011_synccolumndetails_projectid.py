# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20180110_1527'),
        ('syncmaster', '0010_remove_editedcolumnmap_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='synccolumndetails',
            name='projectid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
            preserve_default=False,
        ),
    ]
