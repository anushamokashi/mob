# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-31 10:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_project_table_append_by_underscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleAPISetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('apikey', models.CharField(blank=True, max_length=200, null=True)),
                ('clientid', models.CharField(blank=True, max_length=200, null=True)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]