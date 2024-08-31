from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin import DateFieldListFilter
from django.http import HttpResponse
import nested_admin

import openpyxl

from departments.models import DepartmentEntity
from fals.models import FAL, FALType


from .models import ReceiptRequest, ReceiptRequestCoupon, Certificate, SummaryReport
from .xlsx_export import export_fal_type


class FALInline(GenericTabularInline):
    model = FAL
    autocomplete_fields = ['fal_type']


class DocumentAdmin(admin.ModelAdmin):
    inlines = [FALInline]
    search_fields = ['number', 'sender', 'destination']
    ordering = ['operation_date']
    list_filter = (
        ('operation_date', DateFieldListFilter),
    )
    list_display = ['number', 'sender', 'destination']


class FALNestedInline(nested_admin.NestedGenericTabularInline):
    model = FAL
    autocomplete_fields = ['fal_type']


class DepartmentInline(nested_admin.NestedTabularInline):
    model = DepartmentEntity
    inlines = [FALNestedInline]


class SummaryReportAdmin(nested_admin.NestedModelAdmin):
    inlines = [DepartmentInline]
    search_fields = ['number',]
    ordering = ['operation_date']
    list_filter = (
        ('operation_date', DateFieldListFilter),
    )
    list_display = ['number']


@admin.site.register_view('export-xlsx', 'Експортувати в XLSX', urlname='export_xlsx')
def export_xlsx(request):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=47appendix.xlsx'
    wb = openpyxl.Workbook()
    category = request.GET.get('category')
    fal_types = FALType.objects.filter(
        category=category) if category else FALType.objects.all()
    for fal_type in fal_types:
        ws = wb.create_sheet(fal_type.name.replace('/', ' ')[:30])
        export_fal_type(fal_type, ws)

    wb.save(response)
    return response


admin.site.register(ReceiptRequest, DocumentAdmin)
admin.site.register(ReceiptRequestCoupon, DocumentAdmin)
admin.site.register(Certificate, DocumentAdmin)
admin.site.register(SummaryReport, SummaryReportAdmin)
