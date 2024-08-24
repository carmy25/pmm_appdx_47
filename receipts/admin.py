from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin import DateFieldListFilter
from django.http import HttpResponse

import openpyxl
from openpyxl.utils import get_column_letter


from fals.models import FAL


from .models import ReceiptRequest, ReceiptRequestCoupon


class FALInline(GenericTabularInline):
    model = FAL


class DocumentAdmin(admin.ModelAdmin):
    inlines = [FALInline]
    search_fields = ['number', 'sender', 'destination']
    ordering = ['operation_date']
    list_filter = (
        ('operation_date', DateFieldListFilter),
    )
    list_display = ['number', 'book_number', 'book_series', 'sender']


@admin.site.register_view('export-xlsx', 'Експортувати в XLSX', urlname='export_xlsx')
def export_xlsx(request):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=47appendix.xlsx'
    response.writelines(['heelo', 'wollddd'])
    return response


admin.site.register(ReceiptRequest, DocumentAdmin)
admin.site.register(ReceiptRequestCoupon, DocumentAdmin)
