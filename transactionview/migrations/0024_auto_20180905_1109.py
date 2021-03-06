# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-05 05:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('transactionview', '0023_auto_20180824_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='txnCssutilites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('ionic_header', models.CharField(blank=True, choices=[('fix', 'Fixed Header'), ('flex', 'Flexible Header'), ('noheader', 'No Header')], max_length=100, null=True)),
                ('header_color', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=100, null=True)),
                ('custom_header_title', models.CharField(blank=True, max_length=200, null=True)),
                ('background', models.CharField(blank=True, choices=[('primary', 'Primary'), ('secondary', 'Secondary')], max_length=100, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='component',
            name='click',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='container',
            name='dbtable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='container_dbtable', to='transaction.Txtabledetails'),
        ),
        migrations.AlterField(
            model_name='epost',
            name='projectid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epost_projectid', to='project.Project'),
        ),
        migrations.AlterField(
            model_name='eupdate',
            name='projectid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eupdate_project_id', to='project.Project'),
        ),
        migrations.AlterField(
            model_name='transactionview',
            name='projectid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='txn_projectid', to='project.Project'),
        ),
        migrations.AlterField(
            model_name='transactionview',
            name='transactionid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='txnview_transaction', to='transaction.Transaction'),
        ),
        migrations.AlterField(
            model_name='transactionview',
            name='viewtype',
            field=models.CharField(blank=True, choices=[('carousel', 'Carousel'), ('ng', 'None_Grid'), ('grid', 'Grid'), ('euptxn', 'Eupdate Transactionview')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='txncssutilites',
            name='transactionview',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='css_txn', to='transactionview.Transactionview'),
        ),
    ]
