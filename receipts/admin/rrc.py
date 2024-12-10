
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
    list_display = DocumentAdmin.list_display + ['invoices_count']

    def invoices_count(self, ob):
        return ob.invoices.count()

    invoices_count.short_description = 'К-сть накладних'
