from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from fals.models import FAL


from .models import ReceiptRequest, ReceiptRequestCoupon


class FALInline(GenericTabularInline):
    model = FAL


class DocumentAdmin(admin.ModelAdmin):
    inlines = [FALInline]


admin.site.register(ReceiptRequest, DocumentAdmin)
admin.site.register(ReceiptRequestCoupon, DocumentAdmin)
