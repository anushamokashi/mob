# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-11 07:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0010_txtablecomponentdetails_enum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='parenttransaction',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='primarytable',
        ),
    ]