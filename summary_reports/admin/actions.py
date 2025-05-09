from itertools import chain
from datetime import date
from constance import config

from django.contrib import messages
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from receipts.models.handout_list import HandoutList
from receipts.models.reporting import Reporting


from ..models import (
    HandoutListSummaryReport,
    ReportingSummaryReport,
    InvoiceSummaryReport,
)


def get_last_doc_number(models):
    docs = chain(*[m.objects.all() for m in models])
    sorted_docs = list(sorted(docs, key=lambda r: int(r.number) if r.number else 0))
    if not sorted_docs:
        return 0
    return int(sorted_docs[-1].number) if sorted_docs[-1].number else 0


def prepear_documents(doc_model, queryset):
    last_report_number = get_last_doc_number([doc_model])

    for reporting in queryset:
        reporting_end_day = reporting.end_date.day
        if not reporting.document_date:
            reporting.document_date = (
                date(
                    reporting.end_date.year, reporting.end_date.month, reporting_end_day
                )
                if reporting_end_day > config.REPORTING_DOCUMENT_DATE_DAY
                else date(
                    reporting.end_date.year,
                    reporting.end_date.month,
                    config.REPORTING_DOCUMENT_DATE_DAY,
                )
            )
        if not reporting.number:
            last_report_number += 1
            reporting.number = str(last_report_number)
        reporting.save()


@admin.action(description="Створити зведену відомість")
def create_summary_report(modeladmin, request, queryset):
    last_summary_number = get_last_doc_number(
        [ReportingSummaryReport, InvoiceSummaryReport]
    )
    if (model := modeladmin.model) in (Reporting,):
        prepear_documents(model, queryset)
        queryset = queryset.order_by('start_date')
        start_date = queryset.first().start_date
        end_date = queryset.last().end_date
        '''document_date = (
            end_date
            if end_date.day > config.SUMMARY_REPORT_DOCUMENT_DATE_DAY
            else date(
                end_date.year, end_date.month, config.SUMMARY_REPORT_DOCUMENT_DATE_DAY
            )
        )
        '''
        document_date = end_date
        summary_report_class = (
            ReportingSummaryReport if model is Reporting else HandoutListSummaryReport
        )
        summary_report = summary_report_class(
            number=str(last_summary_number + 1),
            document_date=document_date,
            start_date=start_date,
            end_date=end_date,
        )
    else:
        ordered_query = queryset.order_by("operation_date")
        start_date = ordered_query.first().operation_date
        end_date = ordered_query.last().operation_date
        document_date = (
            end_date
            if end_date.day > config.SUMMARY_REPORT_DOCUMENT_DATE_DAY
            else date(
                end_date.year, end_date.month, config.SUMMARY_REPORT_DOCUMENT_DATE_DAY
            )
        )
        summary_report_class = InvoiceSummaryReport
        if modeladmin.model == HandoutList:
            summary_report_class = HandoutListSummaryReport
    summary_report = summary_report_class(
        number=str(last_summary_number + 1),
        document_date=document_date,
        start_date=start_date,
        end_date=end_date,
    )

    summary_report.save()

    queryset.update(summary_report=summary_report)
    summary_report_url = reverse(
        "admin:%s_%s_change"
        % (summary_report._meta.app_label, summary_report._meta.model_name),
        args=(summary_report.pk,),
    )
    modeladmin.message_user(
        request,
        mark_safe(
            f'Зведену відомість <a href="{summary_report_url}">#{
                summary_report.number}</a> створено'
        ),
        messages.SUCCESS,
    )
