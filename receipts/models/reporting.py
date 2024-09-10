from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from .base import BaseDocument


class Reporting(BaseDocument):
    class Meta:
        verbose_name = 'Донесення'
        verbose_name_plural = 'Донесення'

    operation_date = models.DateField(verbose_name='дата операції')
    number = models.CharField(verbose_name='номер',
                              null=True, blank=True, max_length=50)
