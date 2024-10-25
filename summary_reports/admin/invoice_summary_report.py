from receipts.models.invoice import Invoice

from .base_summary_report import BaseDocumentInline, BaseSummaryReportAdmin


class InvoiceInline(BaseDocumentInline):
    model = Invoice


class InvoiceSummaryReportAdmin(BaseSummaryReportAdmin):
    inlines = [InvoiceInline]
