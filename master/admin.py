from django.contrib import admin
from .models import WidgetType,ComponentType

# Register your models here.
admin.site.register(WidgetType)
admin.site.register(ComponentType)