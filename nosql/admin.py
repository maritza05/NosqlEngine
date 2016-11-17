from django.contrib import admin
from .models import DataModel, Nosql


class DataModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(DataModel, DataModelAdmin)

class NosqlAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'official_website']
    list_filter = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Nosql, NosqlAdmin)