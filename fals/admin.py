from django.contrib import admin

from .models import FAL, FALType


class FALAdmin(admin.ModelAdmin):
    search_fields = ['fal_type__name', 'amount']
    list_display = ['fal_type__name', 'amount']


class FALTypeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category']
    list_display = ['name', 'category']


admin.site.register(FAL, FALAdmin)
admin.site.register(FALType, FALTypeAdmin)
