
from nested_admin import NestedTabularInline

from receipts.admin.document import DocumentAdmin
from receipts.models.receipt import InvoiceForRRC, InvoiceForRRCEntry


class InvoiceForRRCEntryAdmin(NestedTabularInline):
    model = InvoiceForRRCEntry

    autocomplete_fields = ["fal_type"]


class InvoiceForRRCAdmin(NestedTabularInline):
    model = InvoiceForRRC
    exclude = ('certificate',)
    inlines = [InvoiceForRRCEntryAdmin]
    search_fields = ["number"]
    list_display = [
        "number",
    ]


class ReceiptRequestCouponAdmin(DocumentAdmin):
    inlines = DocumentAdmin.inlines + [InvoiceForRRCAdmin]
