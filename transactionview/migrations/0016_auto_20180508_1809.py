# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-08 12:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactionview', '0015_auto_20180430_1747'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='component',
            options={'ordering': ['displayorder']},
        ),
        migrations.AlterModelOptions(
            name='container',
            options={'ordering': ['displayorder']},
        ),
    ]
