from summary_reports.admin.actions import create_summary_report
from .document import DocumentAdmin


class InvoiceAdmin(DocumentAdmin):
    search_fields = ['number', 'sender__name',
                     'destination__name', 'fals__fal_type__name']
    autocomplete_fields = ['sender', 'destination']
    actions = [create_summary_report]
