# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-08 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportsubmit',
            name='click_event',
            field=models.CharField(default='click', max_length=1000),
            preserve_default=False,
        ),
    ]