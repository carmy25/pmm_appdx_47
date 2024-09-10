from django.contrib import admin
from django.http import HttpResponse
from django.contrib import messages

from receipts.models.reporting import FALReportEntry


class FALReportEntry(admin.TabularInline):
    model = FALReportEntry
    autocomplete_fields = ['fal_type']


class ReportingAdmin(admin.ModelAdmin):
    inlines = [FALReportEntry]
    search_fields = ['number', 'department__name']
    list_display = ['department__name', 'start_date', 'end_date']
    actions = ['create_summary_report']

    @admin.action(description="Створити зведену відомість")
    def create_summary_report(self, request, queryset):
        self.message_user(
            request, 'Зведену відомість створено', messages.SUCCESS)
