# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-19 05:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactionview', '0010_auto_20180419_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='epostmapfield',
            name='control_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='epost_control_field', to='transactionview.Component'),
        ),
        migrations.AddField(
            model_name='epostmapfield',
            name='group_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='epost_group_field', to='transactionview.Component'),
        ),
        migrations.AddField(
            model_name='epostmapfield',
            name='is_grid_field',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='epostmapfield',
            name='order_by',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='epostmapfield',
            name='target_fixed_value',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='epostmapfield',
            name='target_row',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]