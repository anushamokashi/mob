# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-16 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactionview', '0004_remove_component_sql_fire_db'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionview',
            name='savetype',
            field=models.CharField(blank=True, choices=[('server', 'Server'), ('client', 'Client')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='component',
            name='widgettype',
            field=models.CharField(blank=True, choices=[('button', 'Button'), ('check', 'Checkbox'), ('date', 'Date'), ('email', 'Email'), ('password', 'Password'), ('number', 'Number'), ('select', 'Select'), ('text', 'Text'), ('time', 'Time'), ('textarea', 'Textarea'), ('radio', 'Radiobox'), ('scan', 'Scan'), ('upload', 'Upload')], max_length=50, null=True),
        ),
    ]
