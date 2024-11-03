from django.contrib import admin

from receipts.admin.inspection_certificate import InspectionCertificateAdmin
from receipts.admin.reporting import ReportingAdmin
from receipts.admin.rrc import InvoiceForRRCAdmin, ReceiptRequestCouponAdmin
from receipts.models.inspection_certificate import InspectionCertificate
from receipts.models.invoice import Invoice
from receipts.models.handout_list import HandoutList
from receipts.models.receipt import InvoiceForRRC
from receipts.models.reporting import Reporting
from receipts.models.writing_off_act import WritingOffAct

from ..models import ReceiptRequest, ReceiptRequestCoupon, Certificate
from .document import DocumentAdmin, HandoutListAdmin
from .invoice import InvoiceAdmin
from .writing_off_act import WritingOffAdmin
from .export_xlsx import export_xlsx


admin.site.register(Reporting, ReportingAdmin)
admin.site.register(ReceiptRequest, DocumentAdmin)
admin.site.register(ReceiptRequestCoupon, ReceiptRequestCouponAdmin)
admin.site.register(Certificate, DocumentAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(HandoutList, HandoutListAdmin)
admin.site.register(WritingOffAct, WritingOffAdmin)
admin.site.register(InspectionCertificate, InspectionCertificateAdmin)
# admin.site.register(InvoiceForRRC, InvoiceForRRCAdmin)

__all__ = [export_xlsx]
