
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from .base import BaseDocument


class Certificate(BaseDocument):
    class Meta:
        verbose_name = 'Атестат'
        verbose_name_plural = 'Атестати'

    sender = models.CharField(verbose_name='відправник', max_length=50)
    destination = models.CharField(verbose_name='отримувач', max_length=50,
                                   default='А4548')
    operation_date = models.DateField(verbose_name='дата операції')
    fals = GenericRelation(
        'fals.FAL', object_id_field='object_id', related_query_name='document')
