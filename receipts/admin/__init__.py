from django.contrib import admin

from receipts.admin.reporting import ReportingAdmin
from receipts.models.reporting import Reporting

from ..models import ReceiptRequest, ReceiptRequestCoupon, Certificate, SummaryReport
from .document import DocumentAdmin, SummaryReportAdmin
from .export_xlsx import export_xlsx


admin.site.register(Reporting, ReportingAdmin)
admin.site.register(ReceiptRequest, DocumentAdmin)
admin.site.register(ReceiptRequestCoupon, DocumentAdmin)
admin.site.register(Certificate, DocumentAdmin)
admin.site.register(SummaryReport, SummaryReportAdmin)

__all__ = [export_xlsx]
