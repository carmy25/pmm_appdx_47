from django.contrib import admin

from summary_reports.models import InvoiceSummaryReport, ReportingSummaryReport

from .reporting_summary_report import ReportingSummaryReportAdmin
from .invoice_summary_report import InvoiceSummaryReportAdmin

from .actions import create_summary_report

admin.site.register(ReportingSummaryReport, ReportingSummaryReportAdmin)
admin.site.register(InvoiceSummaryReport, InvoiceSummaryReportAdmin)
