
from django.db import models

from departments.models import Department
from django.contrib.contenttypes.fields import GenericRelation

from summary_reports.models import HandoutListSummaryReport

from .base import BaseDocument


class HandoutList(BaseDocument):
    class Meta:
        verbose_name = 'Роздавальна відомість'
        verbose_name_plural = 'Роздавальні відомості'
    operation_date = models.DateField(verbose_name='дата операції')

    start_date = models.DateField(verbose_name='початкова дата')
    end_date = models.DateField(verbose_name='кінцева дата')

    sender = models.ForeignKey(
        Department, on_delete=models.CASCADE,
        related_name='hadout_sender',
        verbose_name='відправник')
    destination = models.ForeignKey(
        Department, on_delete=models.CASCADE,
        related_name='handout_receiver',
        verbose_name='отримувач')

    fals = GenericRelation(
        'fals.FAL',
        object_id_field='object_id',
        related_query_name='document')

    summary_report = models.ForeignKey(
        HandoutListSummaryReport,
        null=True, blank=True,
        related_name='handout_lists',
        on_delete=models.SET_NULL)
