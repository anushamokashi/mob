# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-27 05:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0017_auto_20180208_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='txtablecomponentdetails',
            name='datatype',
            field=models.CharField(choices=[('AutoField', 'AutoField'), ('BinaryField', 'BinaryField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DecimalField', 'DecimalField'), ('EmailField', 'EmailField'), ('FileField', 'FileField'), ('ImageField', 'ImageField'), ('IntegerField', 'IntegerField'), ('TextField', 'TextField'), ('CharField', 'CharField'), ('UUIDField', 'UUIDField'), ('ForeignKey_int', 'ForeignKey_int'), ('ForeignKey_char', 'ForeignKey_char'), ('ForeignKey_date', 'ForeignKey_date'), ('Enum_Int', 'Enum_Int'), ('Enum_Char', 'Enum_Char'), ('Enum_Date', 'Enum_Date'), ('ButtonField', 'ButtonField'), ('MacroField', 'MacroField'), ('OneToOneField', 'OneToOneField')], max_length=50),
        ),
    ]
