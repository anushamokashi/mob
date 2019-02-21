# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-27 05:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactionview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiontype', models.CharField(blank=True, choices=[('cancel', 'Cancel'), ('delete', 'Delete'), ('new', 'New'), ('save', 'Save'), ('search', 'Search')], max_length=50, null=True)),
                ('displayorder', models.BigIntegerField(blank=True, null=True)),
                ('transactionviewid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions_type', to='transactionview.Transactionview')),
            ],
        ),
        migrations.CreateModel(
            name='CancelAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('expression', models.TextField(blank=True, null=True)),
                ('expression_postfix', models.TextField(blank=True, null=True)),
                ('iconcls', models.CharField(blank=True, max_length=100, null=True)),
                ('actiontype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cancel_action', to='actions.Actions')),
                ('transactionview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cancel_trans', to='transactionview.Transactionview')),
                ('ui_control_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cancel_ui', to='transactionview.Component')),
            ],
        ),
        migrations.CreateModel(
            name='DeleteAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('expression', models.TextField(blank=True, null=True)),
                ('expression_postfix', models.TextField(blank=True, null=True)),
                ('iconcls', models.CharField(blank=True, max_length=100, null=True)),
                ('actiontype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delete_action', to='actions.Actions')),
                ('transactionview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delete_trans', to='transactionview.Transactionview')),
                ('ui_control_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delete_ui', to='transactionview.Component')),
            ],
        ),
        migrations.CreateModel(
            name='NewAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('expression', models.TextField(blank=True, null=True)),
                ('expression_postfix', models.TextField(blank=True, null=True)),
                ('iconcls', models.CharField(blank=True, max_length=100, null=True)),
                ('actiontype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_action', to='actions.Actions')),
                ('transactionview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_trans', to='transactionview.Transactionview')),
                ('ui_control_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_ui', to='transactionview.Component')),
            ],
        ),
        migrations.CreateModel(
            name='SaveAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('expression', models.TextField(blank=True, null=True)),
                ('expression_postfix', models.TextField(blank=True, null=True)),
                ('iconcls', models.CharField(blank=True, max_length=100, null=True)),
                ('actiontype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='save_action', to='actions.Actions')),
                ('transactionview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='save_trans', to='transactionview.Transactionview')),
                ('ui_control_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='save_ui', to='transactionview.Component')),
            ],
        ),
        migrations.CreateModel(
            name='SearchAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('sql', models.TextField(blank=True, null=True)),
                ('sort_type', models.CharField(blank=True, choices=[('ascending', 'Ascending'), ('descending', 'Descending')], max_length=50, null=True)),
                ('sort_field', models.CharField(blank=True, max_length=100, null=True)),
                ('chunk_size', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('page_size', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('copy_tx_view', models.BooleanField(default=False)),
                ('iconcls', models.CharField(blank=True, max_length=100, null=True)),
                ('actiontype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_action', to='actions.Actions')),
                ('transactionview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_trans', to='transactionview.Transactionview')),
            ],
        ),
    ]
