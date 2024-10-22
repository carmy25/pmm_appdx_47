from django.http import HttpResponse
from summary_reports.forms import MyActionForm

from django.contrib import admin
from admin_object_actions.admin import ModelAdminObjectActionsMixin

from receipts.models.invoice import Invoice

from .base_summary_report import BaseDocumentInline, BaseSummaryReportAdmin


class InvoiceInline(BaseDocumentInline):
    model = Invoice


class InvoiceSummaryReportAdmin(BaseSummaryReportAdmin):
    inlines = [InvoiceInline]
