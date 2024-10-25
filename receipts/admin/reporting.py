from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from receipts.models.reporting import FALReportEntry
from summary_reports.admin.actions import create_summary_report


class FALReportEntry(admin.TabularInline):
    model = FALReportEntry
    autocomplete_fields = ["fal_type"]


class ReportingAdmin(admin.ModelAdmin):
    inlines = [FALReportEntry]
    search_fields = ["number", "department__name"]
    list_display = [
        "number",
        "department__name",
        "start_date",
        "end_date",
        "summary_report",
    ]
    actions = [create_summary_report]
    exclude = ["summary_report"]
    autocomplete_fields = ["department"]
    list_filter = (("end_date", DateRangeFilterBuilder()),)

    def get_ordering(self, request):
        return ["-end_date"]
