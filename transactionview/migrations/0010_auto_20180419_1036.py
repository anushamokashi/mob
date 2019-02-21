# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-19 05:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('transactionview', '0009_epost_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='EpostMapField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.RenameField(
            model_name='epost',
            old_name='transactionview',
            new_name='source_tx_view',
        ),
        migrations.RenameField(
            model_name='epost',
            old_name='targettxview',
            new_name='target_tx_view',
        ),
        migrations.AddField(
            model_name='epostmapfield',
            name='epost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactionview.Epost'),
        ),
        migrations.AddField(
            model_name='epostmapfield',
            name='source_ui_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epost_source_field', to='transactionview.Component'),
        ),
        migrations.AddField(
            model_name='epostmapfield',
            name='target_ui_filed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epost_target_field', to='transactionview.Component'),
        ),
    ]
