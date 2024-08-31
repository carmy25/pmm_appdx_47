from django.contrib import admin

from receipts.admin import FALInline

from .models import Department


class DepartmentAdmin(admin.ModelAdmin):
    # inlines = [FALInline]
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Department, DepartmentAdmin)
