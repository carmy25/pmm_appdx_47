
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseDocument


class ReportingSummaryReport(BaseDocument):
    class Meta:
        verbose_name = 'Зведена відомість по донесеннях'
        verbose_name_plural = 'Зведені відомості по донесеннях'

    start_date = models.DateField(verbose_name='початкова дата')
    end_date = models.DateField(verbose_name='кінцева дата')

    def __str__(self):
        return f'Зведена відомість: {self.number or "без номеру"}'
