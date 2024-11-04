
from nested_admin import NestedTabularInline

from receipts.admin.document import DocumentAdmin
from receipts.admin.rrc import InvoiceForRRCEntryAdmin
from receipts.models.receipt import InvoiceForRRC, InvoiceForRRCEntry


class InvoiceForCertificateAdmin(NestedTabularInline):
    model = InvoiceForRRC
    exclude = ('rrc',)
    inlines = [InvoiceForRRCEntryAdmin]
    search_fields = ["number"]
    list_display = [
        "number",
    ]


class CertificateAdmin(DocumentAdmin):
    inlines = DocumentAdmin.inlines + [InvoiceForCertificateAdmin]
