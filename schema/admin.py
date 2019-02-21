# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Db_connections_info,Db_profile

# Register your models here.
admin.site.register(Db_connections_info)
admin.site.register(Db_profile)