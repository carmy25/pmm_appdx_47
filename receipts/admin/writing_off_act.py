from summary_reports.admin.actions import create_summary_report
from .document import DocumentAdmin


class WritingOffAdmin(DocumentAdmin):
    list_display = [
        'number', 'operation_date', 'scan_present'
    ]
    search_fields = [
        "number",
        "fals__fal_type__name",
    ]
