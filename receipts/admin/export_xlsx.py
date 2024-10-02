
from django.contrib import admin
from django.http import HttpResponse

from departments.models import Department
from fals.models import FALType
from receipts.models.reporting import Reporting
from receipts.xlsx_export.reportings_report import export_reportings_report
from ..xlsx_export import export_fal_type

import openpyxl


def xlsx_response(filename):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
    return response


@admin.site.register_view('export-xlsx', 'Експортувати в Excel', urlname='export_xlsx')
def export_xlsx(request):
    import time
    start = time.time()
    wb = openpyxl.Workbook()
    category = request.GET.get('category')
    fal_types = FALType.objects.filter(
        category=category) if category else FALType.objects.all()
    departments = Department.objects.all().order_by('name')
    for fal_type in fal_types:
        ws = wb.create_sheet(fal_type.name.replace('/', ' ')[:30])
        export_fal_type(fal_type, ws, departments)

    end = time.time()
    print(end - start)
    response = xlsx_response('47appendix')
    wb.save(response)
    print(time.time() - end)
    return response


@admin.site.register_view('reportings-report', 'Звіт по донесеннях', urlname='reportings_report')
def reportings_report(request):
    response = xlsx_response('reportings_report')
    reportings = Reporting.objects.all().order_by('end_date')
    wb = openpyxl.Workbook()
    ws = wb.create_sheet('Звіт')
    if reportings.count() > 0:
        export_reportings_report(ws, reportings)
    wb.save(response)
    return response
