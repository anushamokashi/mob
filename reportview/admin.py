from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Report,ReportParamField

admin.site.register(Report)
admin.site.register(ReportParamField)
