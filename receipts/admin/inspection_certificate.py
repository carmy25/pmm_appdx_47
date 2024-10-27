from .document import DocumentAdmin


class InspectionCertificateAdmin(DocumentAdmin):
    search_fields = [
        "number",
        "department__name",
    ]
    list_display = ['number', 'document_date', 'operation_date', 'department__name']
    autocomplete_fields = ["department"]
