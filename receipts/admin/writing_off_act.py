from .document import DocumentAdmin


class WritingOffAdmin(DocumentAdmin):
    list_display = [
        'number', 'operation_date', 'scan_present'
    ]
    search_fields = [
        "number",
        "fals__fal_type__name",
    ]
