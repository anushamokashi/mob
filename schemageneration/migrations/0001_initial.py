# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-27 05:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('transaction', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenerateSchemaComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('columnname', models.CharField(max_length=100)),
                ('datatype', models.CharField(max_length=50)),
                ('maxlength', models.BigIntegerField()),
                ('no_of_decimal_digits', models.BigIntegerField()),
                ('field_slug', models.CharField(max_length=100)),
                ('isdbfield', models.BooleanField(default=False)),
                ('isnull', models.BooleanField(default=False)),
                ('column', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.Txtablecomponentdetails')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='GenerateSchemaTableComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('tablename', models.CharField(max_length=100)),
                ('table_slug', models.CharField(max_length=100)),
                ('parent', models.CharField(max_length=100)),
                ('ddl_type', models.CharField(choices=[('add', 'add'), ('modify', 'modify'), ('delete', 'delete')], max_length=10)),
                ('projectid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.Txtabledetails')),
                ('transactionid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.Transaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='generateschemacomponent',
            name='gen_schema_table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schemageneration.GenerateSchemaTableComponent'),
        ),
    ]
