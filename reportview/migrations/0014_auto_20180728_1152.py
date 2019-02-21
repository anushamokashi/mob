# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-28 06:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reportview', '0013_auto_20180728_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintFormatActionSQL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sql', models.CharField(blank=True, max_length=500, null=True)),
                ('do', models.PositiveSmallIntegerField(default=0)),
                ('sql_type', models.CharField(choices=[(b'GRID', b'GRID'), (b'NONGRID', b'NONGRID')], max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='reportprintformataction',
            name='sql',
        ),
        migrations.AddField(
            model_name='reportprintformataction',
            name='action_type',
            field=models.CharField(choices=[(b'Server', b'Server'), (b'Client', b'Client')], default='Server', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportprintformataction',
            name='click_event',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='printformatactionsql',
            name='printformataction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reportview.ReportPrintFormatAction'),
        ),
    ]
