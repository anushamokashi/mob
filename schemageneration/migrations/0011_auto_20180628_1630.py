# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-28 11:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schemageneration', '0010_auto_20180208_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generateschematablecomponent',
            name='db_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='generateschematablecomponent',
            name='ddl_type',
            field=models.CharField(blank=True, choices=[('add', 'add'), ('modify', 'modify'), ('delete', 'delete')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='generateschematablecomponent',
            name='projectid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AlterField(
            model_name='generateschematablecomponent',
            name='table_slug',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='generateschematablecomponent',
            name='tablename',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='generateschematablecomponent',
            name='transactionid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.Transaction'),
        ),
        migrations.AlterField(
            model_name='generateschematablecomponent',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile'),
        ),
    ]
