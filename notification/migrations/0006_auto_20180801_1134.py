# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-01 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_notificationconfiguration_user_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationconfiguration',
            name='status_process_type',
            field=models.CharField(blank=True, choices=[('Buttons', 'Buttons'), ('Message', 'Message')], max_length=50, null=True),
        ),
    ]
