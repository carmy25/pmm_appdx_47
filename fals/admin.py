from django.contrib import admin
from django.http import HttpRequest

from .models import FAL, FALType


class FALAdmin(admin.ModelAdmin):
    search_fields = ['fal_type__name', 'amount']
    list_display = ['fal_type__name', 'amount']

    def has_module_permission(self, request: HttpRequest) -> bool:
        return False


class FALTypeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category']
    list_display = ['name', 'category']


admin.site.register(FAL, FALAdmin)
admin.site.register(FALType, FALTypeAdmin)
