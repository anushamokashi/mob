# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-05 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printformat', '0002_remove_printformat_iconcls'),
    ]

    operations = [
        migrations.AddField(
            model_name='printformat',
            name='slug',
            field=models.CharField(default='sample', max_length=100),
            preserve_default=False,
        ),
    ]
