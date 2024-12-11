from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

from receipts.models.reporting import FALReportEntry
from summary_reports.admin.actions import create_summary_report


class FALReportEntry(admin.TabularInline):
    model = FALReportEntry
    autocomplete_fields = ["fal_type"]


class ReportingAdmin(admin.ModelAdmin):
    inlines = [FALReportEntry]
    search_fields = ["number", "department__name", 'fals__fal_type__name']
    list_display = [
        "number",
        "department__name",
        "start_date",
        "end_date",
        "summary_report",
        'last_updated'
    ]
    actions = [create_summary_report]
    exclude = ["summary_report"]
    autocomplete_fields = ["department"]
    list_filter = (("end_date", DateRangeFilterBuilder()),)

    def get_ordering(self, request):
        return ["-end_date"]

    def last_updated(self, obj):
        le_obj = LogEntry.objects.filter(
            object_id=obj.id,
            content_type=ContentType.objects.get(
                model=obj._meta.object_name.lower(),
                app_label=obj._meta.app_label)).order_by('-action_time').first()
        return le_obj.action_time

    last_updated.short_description = 'Востаннє Оновлено'
