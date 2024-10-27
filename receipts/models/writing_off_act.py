from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from .base import BaseDocument


class WritingOffAct(BaseDocument):
    class Meta:
        verbose_name = "акт списання"
        verbose_name_plural = "акти списання"

    number = models.CharField(
        verbose_name="номер", null=True, blank=True, max_length=50
    )
    operation_date = models.DateField(verbose_name="дата операції", null=True, blank=True)

    fals = GenericRelation(
        "fals.FAL", object_id_field="object_id", related_query_name="document"
    )
