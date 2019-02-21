# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-05 09:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20180110_1527'),
        ('syncmaster', '0003_editeduserslist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='synccolumndetails',
            options={},
        ),
        migrations.AlterModelOptions(
            name='synctabledetails',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='synccolumndetails',
            unique_together=set([('syncTable', 'sourcefield', 'targetfield')]),
        ),
        migrations.AlterUniqueTogether(
            name='synctabledetails',
            unique_together=set([('projectid', 'sourcetable', 'targettable')]),
        ),
    ]