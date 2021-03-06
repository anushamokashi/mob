# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-03 11:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eventconfiguration', '0002_auto_20180903_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='txnmappingforevent',
            name='event_start_day',
            field=models.ForeignKey(default=40, on_delete=django.db.models.deletion.CASCADE, related_name='event_start_day', to='transactionview.Component'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='txnmappingforevent',
            name='event_title',
            field=models.ForeignKey(default=40, on_delete=django.db.models.deletion.CASCADE, related_name='event_title', to='transactionview.Component'),
            preserve_default=False,
        ),
    ]
