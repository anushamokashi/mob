# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-05 07:11
from __future__ import unicode_literals

from django.db import migrations, models
import printformat.models


class Migration(migrations.Migration):

    dependencies = [
        ('printformat', '0004_auto_20180905_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='printformat',
            name='cssfile',
            field=models.FileField(default='css.html', upload_to=printformat.models.user_directory_path),
            preserve_default=False,
        ),
    ]
