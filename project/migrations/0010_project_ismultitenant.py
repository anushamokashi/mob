# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-05 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_googleapisetup'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='ismultitenant',
            field=models.BooleanField(default=False),
        ),
    ]
