# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-28 07:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20180112_1054'),
        ('transaction', '0019_auto_20180628_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='txtablecomponentdetails',
            name='user',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='txtabledetails',
            name='user',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile'),
            preserve_default=False,
        ),
    ]