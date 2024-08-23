from django.contrib import admin

from .models import ReceiptRequest, ReceiptRequestCoupon

admin.site.register(ReceiptRequest)
admin.site.register(ReceiptRequestCoupon)
