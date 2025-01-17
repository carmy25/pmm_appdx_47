from django.contrib import admin
from admin_object_actions.admin import ModelAdminObjectActionsMixin
from django.http import HttpResponse
import openpyxl

from receipts.admin.export_xlsx import xlsx_response
from summary_reports.forms import MyActionForm
from xlsx_export.summary_report import export_summary_report


class BaseSummaryReportAdmin(ModelAdminObjectActionsMixin, admin.ModelAdmin):
    search_fields = ["number"]
    list_display = [
        "number",
        "start_date",
        "end_date",
        "display_object_actions_list",
    ]
    readonly_fields = ("display_object_actions_detail",)

    object_actions = [
        {
            "slug": "generate-xlsx",
            "verbose_name": "Завантажити",
            "form_method": "GET",
        },
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def object_action_view(self, request, action, object_id):
        response = xlsx_response(f'summary_report_{object_id}')
        wb = openpyxl.Workbook()
        ws = wb['Sheet']
        ws.title = 'Звередна по донесеннях'
        export_summary_report(ws, self.model.objects.get(id=object_id))
        wb.save(response)
        return response

    def display_object_actions_detail(self, obj):
        return super().display_object_actions_detail(obj)

    display_object_actions_detail.short_description = "Дії"


class BaseDocumentInline(admin.TabularInline):
    show_change_link = True
    # readonly_fields = ['number', 'start_date', 'end_date',]

    def has_change_permission(self, request, obj):
        return False

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False
