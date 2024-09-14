from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from departments.models import Department

from .base import BaseDocument


class Invoice(BaseDocument):
    class Meta:
        verbose_name = 'Накладна'
        verbose_name_plural = 'Накладні'

    operation_date = models.DateField(verbose_name='дата операції')
    sender = models.ForeignKey(
        Department, on_delete=models.CASCADE,
        related_name='invoices_sender',
        verbose_name='відправник')
    receiver = models.ForeignKey(
        Department, on_delete=models.CASCADE,
        related_name='invoices_receiver',
        verbose_name='отримувач')
    responsible_person = models.CharField(
        verbose_name='відповідальна особа', max_length=233)
    fals = GenericRelation(
        'fals.FAL',
        object_id_field='object_id',
        related_name='document')
