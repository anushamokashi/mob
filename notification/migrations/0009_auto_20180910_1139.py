# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-10 06:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0008_auto_20180817_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='creatingJson',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notificationconfiguration',
            name='basicid_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_basicid_field', to='transactionview.Component'),
        ),
    ]
