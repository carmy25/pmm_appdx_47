from django.contrib import admin
from django.http import HttpRequest
import openpyxl

from receipts.admin.export_xlsx import xlsx_response
from xlsx_export.fals_report import export_fals_report

from .models import FAL, FALType


class FALAdmin(admin.ModelAdmin):
    search_fields = ["fal_type__name", "amount"]
    list_display = ["fal_type__name", "amount"]

    def has_module_permission(self, request: HttpRequest) -> bool:
        return False


class FALTypeAdmin(admin.ModelAdmin):
    search_fields = ["name", "category"]
    list_display = ["name", "category", "density"]


admin.site.register(FAL, FALAdmin)
admin.site.register(FALType, FALTypeAdmin)


@admin.site.register_view(
    "fals-report", "Звіт по паливу", urlname="fals_report"
)
def fal_report(request):
    response = xlsx_response("fals_report")
    wb = openpyxl.Workbook()
    ws = wb['Sheet']
    ws.title = 'Звіт по паливу'
    export_fals_report(ws,
                       FALType.objects.all().order_by('name').order_by('category'))
    wb.save(response)
    return response
