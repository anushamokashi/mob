# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-26 06:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20180224_1547'),
        ('transactionview', '0012_auto_20180426_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Epost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('based_on_container', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactionview.Container')),
                ('projectid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('source_tx_view', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='epost_src_txview', to='transactionview.Transactionview')),
                ('target_tx_view', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='epost_target_txview', to='transactionview.Transactionview')),
                ('ui_control_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactionview.Component')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='EpostMapField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('target_fixed_value', models.CharField(blank=True, max_length=500, null=True)),
                ('is_grid_field', models.BooleanField(default=False)),
                ('order_by', models.BigIntegerField(blank=True, null=True)),
                ('control_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='epost_control_field', to='transactionview.Component')),
                ('epost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactionview.Epost')),
                ('group_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='epost_group_field', to='transactionview.Component')),
                ('source_ui_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='epost_source_field', to='transactionview.Component')),
                ('target_ui_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='epost_target_field', to='transactionview.Component')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.RenameField(
            model_name='eupdate',
            old_name='target_ui_filed',
            new_name='target_ui_field',
        ),
    ]
