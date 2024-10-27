from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from departments.models import Department

from .base import BaseDocument


class InspectionCertificate(BaseDocument):
    class Meta:
        verbose_name = "Інспекторське Посвідчення"
        verbose_name_plural = "Інспекторські Посвідчення"

    number = models.CharField(
        verbose_name="номер", null=True, blank=True, max_length=50
    )
    operation_date = models.DateField(verbose_name="дата операції")
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, verbose_name="підрозділ"
    )
