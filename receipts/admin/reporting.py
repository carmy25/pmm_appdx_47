from django.contrib import admin
from django.http import HttpResponse
from django.contrib import messages

from receipts.models.reporting import FALReportEntry
from receipts.models.summary_report import ReportingSummaryReport

import datetime


class FALReportEntry(admin.TabularInline):
    model = FALReportEntry
    autocomplete_fields = ['fal_type']


class ReportingAdmin(admin.ModelAdmin):
    inlines = [FALReportEntry]
    search_fields = ['number', 'department__name']
    list_display = ['department__name',
                    'start_date', 'end_date', 'summary_report']
    actions = ['create_summary_report']
    exclude = ['summary_report']

    @admin.action(description="Створити зведену відомість")
    def create_summary_report(self, request, queryset):
        summary_report = ReportingSummaryReport(
            number='23', start_date=datetime.datetime.now(), end_date=datetime.datetime.now())
        summary_report.save()
        queryset.update(summary_report=summary_report)
        self.message_user(
            request, 'Зведену відомість створено', messages.SUCCESS)
