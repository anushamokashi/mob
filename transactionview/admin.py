# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Transactionview,Container,Component
# Register your models here.
class TransactionviewAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'title',
        'description',
        'viewtype',
        'transactionid',
        'projectid',
       
    )

    def has_add_permission(self, request):
        if self.model.objects.count() == 0:
            return True
        else:
            return False
    search_fields = ('title',)
admin.site.register(Transactionview, TransactionviewAdmin)

class ContainerAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'title',
        'caption',
        'containertype',
        'inputtype',
        'parent',
        'transactionviewid',
        'displayorder',
       
    )
    search_fields = ('title',)
admin.site.register(Container, ContainerAdmin)


class ComponentAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'title',
        'caption',
        'is_readonly',
        'is_hidden',
        'is_required',
        'allow_duplicate',
        'widgettype',
        'expression',
        'validateexp',
        'sql',
        'displayorder',
        'containerid',
        'transactionviewid',
        'identifiers',
        'componentrefer_id',
        'componenttype', 
        'dbcolumn',
        'componentrefer_dt',
        'modeOfEntry',     
        'suggestive',                       
    )
    search_fields = ('title',)
admin.site.register(Component, ComponentAdmin)
