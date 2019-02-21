# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-27 05:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='statusOfTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'new'), ('modified', 'modified'), ('deleted', 'deleted')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txname', models.CharField(max_length=100)),
                ('txdescription', models.CharField(max_length=200)),
                ('parenttransaction', models.CharField(max_length=250)),
                ('primarytable', models.CharField(blank=True, max_length=250, null=True)),
                ('projectid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Txtablecomponentdetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('columnname', models.CharField(max_length=100)),
                ('datatype', models.CharField(choices=[('AutoField', 'AutoField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DecimalField', 'DecimalField'), ('EmailField', 'EmailField'), ('ImageField', 'ImageField'), ('IntegerField', 'IntegerField'), ('TextField', 'TextField'), ('UUIDField', 'UUIDField'), ('ForeignKey_int', 'ForeignKey_int'), ('ForeignKey_char', 'ForeignKey_char'), ('ForeignKey_date', 'ForeignKey_date'), ('Enum_Int', 'Enum_Int'), ('Enum_Char', 'Enum_Char'), ('Enum_Date', 'Enum_Date'), ('ButtonField', 'ButtonField'), ('MacroField', 'MacroField'), ('OneToOneField', 'OneToOneField')], max_length=50)),
                ('maxlength', models.BigIntegerField()),
                ('no_of_decimal_digits', models.BigIntegerField()),
                ('field_slug', models.CharField(max_length=100)),
                ('isdbfield', models.BooleanField(default=False)),
                ('isnull', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Txtabledetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('tablename', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('relationshiptype', models.CharField(blank=True, choices=[('one-to-one', 'One-to-One'), ('one-to-many', 'One-to-Many')], max_length=50, null=True)),
                ('isprimary', models.BooleanField(default=True)),
                ('table_slug', models.CharField(max_length=100)),
                ('projectid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('transactionid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_url_params', to='transaction.Transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='txtablecomponentdetails',
            name='txtabledetailid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_url_params', to='transaction.Txtabledetails'),
        ),
        migrations.AddField(
            model_name='statusoftable',
            name='columnId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.Txtablecomponentdetails'),
        ),
        migrations.AddField(
            model_name='statusoftable',
            name='projectId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='statusoftable',
            name='tableId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.Txtabledetails'),
        ),
        migrations.AddField(
            model_name='statusoftable',
            name='transactionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.Transaction'),
        ),
    ]
