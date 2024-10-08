from constance import config
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import admin
from django.contrib import messages

from receipts.models.reporting import FALReportEntry, Reporting
from summary_reports.models import ReportingSummaryReport

from datetime import date


class FALReportEntry(admin.TabularInline):
    model = FALReportEntry
    autocomplete_fields = ['fal_type']


class ReportingAdmin(admin.ModelAdmin):
    inlines = [FALReportEntry]
    search_fields = ['number', 'department__name']
    list_display = ['number',
                    'department__name',
                    'start_date', 'end_date', 'summary_report']
    actions = ['create_summary_report']
    exclude = ['summary_report']
    autocomplete_fields = ['department']

    def get_last_doc_number(self, model):
        sorted_docs = list(sorted(model.objects.all(),
                                  key=lambda r: int(r.number) if r.number else 0))
        if not sorted_docs:
            return 0
        return int(sorted_docs[-1].number) if sorted_docs[-1].number else 0

    def prepear_reportings(self, queryset):
        last_report_number = self.get_last_doc_number(Reporting)

        for reporting in queryset:
            reporting_end_day = reporting.end_date.day
            if not reporting.document_date:
                reporting.document_date = \
                    date(reporting.end_date.year,
                         reporting.end_date.month,
                         reporting_end_day) if reporting_end_day > config.REPORTING_DOCUMENT_DATE_DAY \
                    else date(reporting.end_date.year, reporting.end_date.month, config.REPORTING_DOCUMENT_DATE_DAY)
            if not reporting.number:
                last_report_number += 1
                reporting.number = str(last_report_number)
            reporting.save()

    @admin.action(description="Створити зведену відомість")
    def create_summary_report(self, request, queryset):
        self.prepear_reportings(queryset)

        last_summary_number = self.get_last_doc_number(ReportingSummaryReport)

        start_date = queryset.order_by('start_date').first().start_date
        end_date = queryset.order_by('-end_date').first().end_date
        document_date =  \
            end_date if end_date.day > config.SUMMARY_REPORT_DOCUMENT_DATE_DAY \
            else date(end_date.year, end_date.month, config.SUMMARY_REPORT_DOCUMENT_DATE_DAY)

        summary_report = ReportingSummaryReport(
            number=str(last_summary_number+1),
            document_date=document_date,
            start_date=start_date,
            end_date=end_date)
        summary_report.save()

        queryset.update(summary_report=summary_report)
        summary_report_url = reverse('admin:%s_%s_change' % (
            summary_report._meta.app_label, summary_report._meta.model_name), args=(summary_report.pk,))
        self.message_user(
            request, mark_safe(f'Зведену відомість <a href="{summary_report_url}">#{summary_report.number}</a> створено'), messages.SUCCESS)
