
from receipts.models.handout_list import HandoutList

from .base_summary_report import BaseDocumentInline, BaseSummaryReportAdmin


class HandoutListInline(BaseDocumentInline):
    model = HandoutList


class HandoutListSummaryReportAdmin(BaseSummaryReportAdmin):
    inlines = [HandoutListInline]
