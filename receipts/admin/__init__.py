from django.contrib import admin

from receipts.admin.reporting import ReportingAdmin
from receipts.models.invoice import Invoice
from receipts.models.handout_list import HandoutList
from receipts.models.reporting import Reporting

from ..models import ReceiptRequest, ReceiptRequestCoupon, Certificate
from .document import DocumentAdmin, HandoutListAdmin
from .invoice import InvoiceAdmin
from .export_xlsx import export_xlsx


admin.site.register(Reporting, ReportingAdmin)
admin.site.register(ReceiptRequest, DocumentAdmin)
admin.site.register(ReceiptRequestCoupon, DocumentAdmin)
admin.site.register(Certificate, DocumentAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(HandoutList, HandoutListAdmin)

__all__ = [export_xlsx]
