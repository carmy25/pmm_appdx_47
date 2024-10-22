
from receipts.models.reporting import Reporting

from .base_summary_report import BaseDocumentInline, BaseSummaryReportAdmin


class ReportingInline(BaseDocumentInline):
    model = Reporting


class ReportingSummaryReportAdmin(BaseSummaryReportAdmin):
    inlines = [ReportingInline]
