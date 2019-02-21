# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-03 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20180102_1813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enumtitle',
            old_name='title',
            new_name='enum_title',
        ),
        migrations.AlterField(
            model_name='txtablecomponentdetails',
            name='datatype',
            field=models.CharField(choices=[('AutoField', 'AutoField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DecimalField', 'DecimalField'), ('EmailField', 'EmailField'), ('ImageField', 'ImageField'), ('IntegerField', 'IntegerField'), ('TextField', 'TextField'), ('CharField', 'CharField'), ('UUIDField', 'UUIDField'), ('ForeignKey_int', 'ForeignKey_int'), ('ForeignKey_char', 'ForeignKey_char'), ('ForeignKey_date', 'ForeignKey_date'), ('Enum_Int', 'Enum_Int'), ('Enum_Char', 'Enum_Char'), ('Enum_Date', 'Enum_Date'), ('ButtonField', 'ButtonField'), ('MacroField', 'MacroField'), ('OneToOneField', 'OneToOneField')], max_length=50),
        ),
        migrations.AlterField(
            model_name='txtablecomponentdetails',
            name='isdbfield',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='txtablecomponentdetails',
            name='isnull',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='txtablecomponentdetails',
            name='no_of_decimal_digits',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='txtabledetails',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
