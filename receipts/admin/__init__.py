from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

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
from .certificate import CertificateAdmin
from .writing_off_act import WritingOffAdmin
from .export_xlsx import export_xlsx


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_link', 'action_flag', 'change_message')
    list_filter = ('user', 'content_type', 'action_flag')
    search_fields = ('object_repr', 'change_message', 'user__username')

    def object_link(self, obj):
        if obj.action_flag == 3 or not obj.object_id:  # deletion or missing
            return obj.object_repr
        try:
            ct = ContentType.objects.get_for_id(obj.content_type_id)
            model_class = ct.model_class()
            instance = model_class.objects.get(pk=obj.object_id)
            return f'<a href="/admin/{ct.app_label}/{ct.model}/{obj.object_id}/change/">{obj.object_repr}</a>'
        except Exception:
            return obj.object_repr
    object_link.allow_tags = True
    object_link.short_description = 'Object'

admin.site.register(LogEntry, LogEntryAdmin)



admin.site.register(Reporting, ReportingAdmin)
admin.site.register(ReceiptRequest, DocumentAdmin)
admin.site.register(ReceiptRequestCoupon, ReceiptRequestCouponAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(HandoutList, HandoutListAdmin)
admin.site.register(WritingOffAct, WritingOffAdmin)
admin.site.register(InspectionCertificate, InspectionCertificateAdmin)

__all__ = [export_xlsx]
