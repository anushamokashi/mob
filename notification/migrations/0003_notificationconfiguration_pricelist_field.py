# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-09 05:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactionview', '0016_auto_20180508_1809'),
        ('notification', '0002_notificationconfiguration_choosed_status_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationconfiguration',
            name='pricelist_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_pricelist_field', to='transactionview.Component'),
        ),
    ]
