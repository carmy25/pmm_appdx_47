from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin import DateFieldListFilter

from fals.models import FAL


from .models import ReceiptRequest, ReceiptRequestCoupon


class FALInline(GenericTabularInline):
    model = FAL


class DocumentAdmin(admin.ModelAdmin):
    inlines = [FALInline]
    search_fields = ['number', 'sender', 'destination']
    ordering = ['operation_date']
    list_filter = (
        ('operation_date', DateFieldListFilter),
    )


admin.site.register(ReceiptRequest, DocumentAdmin)
admin.site.register(ReceiptRequestCoupon, DocumentAdmin)
