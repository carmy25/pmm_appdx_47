from django.contrib import admin

from .models import Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Department, DepartmentAdmin)
