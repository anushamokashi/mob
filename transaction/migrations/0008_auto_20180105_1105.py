# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-05 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_txtablecomponentdetails_is_system_component'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enumtitle',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
