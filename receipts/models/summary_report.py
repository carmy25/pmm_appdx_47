
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from .base import BaseDocument


class SummaryReport(BaseDocument):
    class Meta:
        verbose_name = 'Зведена відомість'
        verbose_name_plural = 'Зведені відомості'

    operation_date = models.DateField(verbose_name='дата операції')
