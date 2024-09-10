
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _


class BaseDocument(models.Model):
    number = models.CharField(verbose_name='номер', max_length=50)
    document_date = models.DateField(
        verbose_name='дата документу', null=True, blank=True)
    scan = models.FileField(null=True, blank=True, verbose_name='Скан')

    class Meta:
        abstract = True

    def verbose_scan_present(self):
        return 'Так' if self.scan.name else 'Ні'
    verbose_scan_present.short_description = 'Скан присутній'
