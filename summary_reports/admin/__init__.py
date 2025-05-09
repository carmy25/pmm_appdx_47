from django.contrib import admin

from summary_reports.admin.handout_list_summary_report import (
    HandoutListSummaryReportAdmin,
)
from summary_reports.models import (
    HandoutListSummaryReport,
    InvoiceSummaryReport,
    ReportingSummaryReport,
)

from .reporting_summary_report import ReportingSummaryReportAdmin
from .invoice_summary_report import InvoiceSummaryReportAdmin

admin.site.register(ReportingSummaryReport, ReportingSummaryReportAdmin)
admin.site.register(InvoiceSummaryReport, InvoiceSummaryReportAdmin)
admin.site.register(HandoutListSummaryReport, HandoutListSummaryReportAdmin)
