# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-17 13:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0007_auto_20180801_1528'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notificationconfiguration',
            old_name='pricelist_field',
            new_name='basicid_field',
        ),
    ]
