# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-24 09:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0015_remove_txtabledetails_db'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='txtablecomponentdetails',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='txtablecomponentdetails',
            unique_together=set([('columnname', 'txtabledetailid')]),
        ),
    ]
