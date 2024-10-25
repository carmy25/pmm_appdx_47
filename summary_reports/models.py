from django.db import models

from receipts.models.base import BaseDocument


class BaseSummaryReport(BaseDocument):
    class Meta:
        abstract = True

    start_date = models.DateField(verbose_name="початкова дата")
    end_date = models.DateField(verbose_name="кінцева дата")

    def __str__(self):
        return f'Зведена відомість: {self.number or "без номеру"}'


class ReportingSummaryReport(BaseSummaryReport):
    class Meta:
        verbose_name = "Зведена відомість по донесеннях"
        verbose_name_plural = "Зведені відомості по донесеннях"


class InvoiceSummaryReport(BaseSummaryReport):
    class Meta:
        verbose_name = "Зведена відомість по накладних"
        verbose_name_plural = "Зведені відомості по накладних"


class HandoutListSummaryReport(BaseSummaryReport):
    class Meta:
        verbose_name = "Зведена відомість по роздавальних"
        verbose_name_plural = "Зведені відомості по роздавальних"
