# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-04 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemageneration', '0007_auto_20180104_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generateschemacomponent',
            name='no_of_decimal_digits',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
