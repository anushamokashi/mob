# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-26 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0023_auto_20180705_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='txdescription',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
