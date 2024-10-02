from django.contrib import admin

from .models import Department, Warehouse


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
