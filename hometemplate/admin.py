# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Homepage,Menu
# Register your models here.
class HomepageAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'menutype',
        'column',
        'sidemenu',
        'project_id',  
    )
    search_fields = ('project_id',)
admin.site.register(Homepage, HomepageAdmin)

class MenuAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'title',
        'description',
        'iconcls',
        'typeofview',
        'transactionview',
        'reportview',
        'homepageid',
        'createpage'

    )
    search_fields = ('title',)
admin.site.register(Menu, MenuAdmin)
