# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-25 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportview', '0028_reportparamfield_sql'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='graphtype',
            field=models.CharField(blank=True, choices=[(b'column', b'Column chart'), (b'line', b'Line chart'), (b'pie', b'Pie chart'), (b'bar', b'Bar chart'), (b'horizontalBar', b'Horizontal Bar')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='reportparamfield',
            name='sql',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
