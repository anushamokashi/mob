# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Transaction,Txtabledetails,Txtablecomponentdetails
# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'txname',
        'txdescription',
        'projectid',
       
    )
    search_fields = ('txname',)
admin.site.register(Transaction, TransactionAdmin)

class TxtabledetailsAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'title',
        'tablename',
        'description',
        'relationshiptype',
        'transactionid',
        'isprimary',
        'table_slug'
       
    )
    search_fields = ('title',)
admin.site.register(Txtabledetails, TxtabledetailsAdmin)


class TxtablecomponentdetailsAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'title',
        'txtabledetailid',
        'columnname',
        'datatype',
        'no_of_decimal_digits',
        'field_slug',
        'isdbfield',
        'isnull',
       
    )
    search_fields = ('title',)
admin.site.register(Txtablecomponentdetails, TxtablecomponentdetailsAdmin)
