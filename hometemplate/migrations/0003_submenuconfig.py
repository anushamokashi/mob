# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-04 13:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_project_imei_based_login'),
        ('hometemplate', '0002_auto_20180905_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubMenuConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('Caption', models.CharField(max_length=100)),
                ('menuaction', models.CharField(choices=[('menu', 'From Menu'), ('other', 'Other')], max_length=50)),
                ('expression', models.CharField(blank=True, max_length=200, null=True)),
                ('displayorder', models.BigIntegerField()),
                ('homepageid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submenu3_url_params', to='hometemplate.Homepage')),
                ('pageValue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submenu_url_params', to='hometemplate.Menu')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submenu2_url_params', to='project.Project')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
