from django.contrib import admin

from receipts.admin.reporting import ReportingAdmin
from receipts.models.invoice import Invoice
from receipts.models.reporting import Reporting
from receipts.models.summary_report import ReportingSummaryReport

from ..models import ReceiptRequest, ReceiptRequestCoupon, Certificate
from .document import DocumentAdmin, InvoiceAdmin
from .reporting_summary_report import ReportingSummaryReportAdmin
from .export_xlsx import export_xlsx


admin.site.register(Reporting, ReportingAdmin)
admin.site.register(ReceiptRequest, DocumentAdmin)
admin.site.register(ReceiptRequestCoupon, DocumentAdmin)
admin.site.register(Certificate, DocumentAdmin)
admin.site.register(ReportingSummaryReport, ReportingSummaryReportAdmin)
admin.site.register(Invoice, InvoiceAdmin)

__all__ = [export_xlsx]
