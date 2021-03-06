# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-05 05:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0002_auto_20180110_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyncColumnDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('sourcefield', models.CharField(blank=True, max_length=200, null=True)),
                ('targetfield', models.CharField(blank=True, max_length=200, null=True)),
                ('WHERECON', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='SyncTableDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('sourcetable', models.CharField(blank=True, max_length=200, null=True)),
                ('targettable', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('dependson', models.CharField(blank=True, max_length=200, null=True)),
                ('orderno', models.BigIntegerField(blank=True, null=True)),
                ('projectid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syncproject', to='project.Project')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='synccolumndetails',
            name='syncTable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='synccolumn', to='syncmaster.SyncTableDetails'),
        ),
    ]
