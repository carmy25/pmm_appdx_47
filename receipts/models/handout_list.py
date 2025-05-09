from django.db import models

from departments.models import Department
from django.contrib.contenttypes.fields import GenericRelation

from summary_reports.models import HandoutListSummaryReport

from .base import BaseDocument


class HandoutList(BaseDocument):
    class Meta:
        verbose_name = "Роздавальна відомість"
        verbose_name_plural = "Роздавальні відомості"

    number = models.CharField(verbose_name="номер", max_length=50, null=True, blank=True)

    operation_date = models.DateField(verbose_name="дата операції")

    start_date = models.DateField(verbose_name="початкова дата", blank=True, null=True)
    end_date = models.DateField(verbose_name="кінцева дата", blank=True, null=True)

    sender = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="sent_handouts",
        verbose_name="відправник",
    )
    destination = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="received_handouts",
        verbose_name="отримувач",
    )

    fals = GenericRelation(
        "fals.FAL", object_id_field="object_id", related_query_name="document"
    )

    summary_report = models.ForeignKey(
        HandoutListSummaryReport,
        null=True,
        blank=True,
        related_name="documents",
        on_delete=models.SET_NULL,
        verbose_name="зведена відомість",
    )
