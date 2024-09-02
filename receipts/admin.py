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


class ScanListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'найвністю скану документу'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "have_scan"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("scan_present", 'Cкан документа присутній'),
            ("scan_absent", 'Без скану документа'),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if queryset.model is Certificate:
            return queryset
        scan_present_qs = queryset.exclude(
            scan__isnull=True).exclude(scan__exact='')
        if self.value() == "scan_present":
            return scan_present_qs
        if self.value() == "scan_absent":
            return queryset.exclude(scan__isnull=False).exclude(scan__exact='')


class DocumentAdmin(admin.ModelAdmin):
    inlines = [FALInline]
    search_fields = ['number', 'sender', 'destination']
    ordering = ['operation_date']
    list_filter = (
        ScanListFilter,
        ('operation_date', DateFieldListFilter),
    )
    list_display = ['number', 'sender', 'destination', 'book']

    def book(self, obj):
        if type(obj) == Certificate:
            return ''
        return f'{obj.book_number}{obj.book_series.upper()}'
    book.short_description = 'Книга'


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
