
from django.contrib import admin
from django.http import HttpResponse

from departments.models import Department
from fals.models import FALType
from ..xlsx_export import export_fal_type

import openpyxl


@admin.site.register_view('export-xlsx', 'Експортувати в XLSX', urlname='export_xlsx')
def export_xlsx(request):
    import time
    start = time.time()
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=47appendix.xlsx'
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
    wb.save(response)
    print(time.time() - end)
    return response
