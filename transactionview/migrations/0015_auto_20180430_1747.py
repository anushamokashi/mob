# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-30 12:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactionview', '0014_auto_20180430_1229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='epostmapfield',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='epostmapfield',
            unique_together=set([('epost', 'order_by')]),
        ),
    ]
