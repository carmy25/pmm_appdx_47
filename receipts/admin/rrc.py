
from django.contrib import admin
from django.http import HttpRequest
from nested_admin import NestedInlineModelAdmin, NestedTabularInline

from receipts.admin.document import DocumentAdmin
from receipts.models.receipt import InvoiceForRRC, InvoiceForRRCEntry


class InvoiceForRRCEntryAdmin(NestedTabularInline):
    model = InvoiceForRRCEntry

    autocomplete_fields = ["fal_type"]


class InvoiceForRRCAdmin(NestedTabularInline):
    model = InvoiceForRRC
    inlines = [InvoiceForRRCEntryAdmin]
    search_fields = ["number"]
    list_display = [
        "number",
    ]


class ReceiptRequestCouponAdmin(DocumentAdmin):
    inlines = DocumentAdmin.inlines + [InvoiceForRRCAdmin]
