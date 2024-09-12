from constance import config

from django.contrib import admin
from django.contrib import messages

from receipts.models.reporting import FALReportEntry, Reporting
from receipts.models.summary_report import ReportingSummaryReport

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

    def prepear_reportings(self, queryset):
        last_report = list(sorted(Reporting.objects.all(),
                                  key=lambda r: int(r.number) if r.number else 1))
        if not last_report:
            last_report_number = 1
        else:
            last_report_number = int(
                last_report[-1].number) if last_report[-1].number else 1

        for reporting in queryset:
            last_report_number += 1
            reporting_end_day = reporting.end_date.day
            if not reporting.document_date:
                reporting.document_date = \
                    date(reporting.end_date.year,
                         reporting.end_date.month,
                         reporting_end_day) if reporting_end_day > config.REPORTING_DOCUMENT_DATE_DAY \
                    else date(reporting.end_date.year, reporting.end_date.month, config.REPORTING_DOCUMENT_DATE_DAY)
            reporting.number = str(last_report_number)
            reporting.save()

    @admin.action(description="Створити зведену відомість")
    def create_summary_report(self, request, queryset):
        self.prepear_reportings(queryset)

        last_summary = list(sorted(ReportingSummaryReport.objects.all(),
                                   key=lambda r: int(r.number) if r.number else 1))
        if not last_summary or last_summary[-1].number is None:
            last_summary_number = 1
        else:
            last_summary_number = int(last_summary[-1].number)

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
        self.message_user(
            request, f'Зведену відомість #{summary_report.number} створено', messages.SUCCESS)
