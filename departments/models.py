from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Department(models.Model):
    class Meta:
        verbose_name = 'Підрозділ'
        verbose_name_plural = 'Підрозділи'

    name = models.CharField(max_length=100, verbose_name="ім'я")

    def __str__(self):
        return self.name


class DepartmentEntity(models.Model):
    class Meta:
        verbose_name = 'Підрозділ'
        verbose_name_plural = 'Підрозділи'

    fals = GenericRelation(
        'fals.FAL', object_id_field='object_id', related_query_name='department')
    department = models.ForeignKey(
        Department, verbose_name="ім'я", on_delete=models.CASCADE)

    summary_report = models.ForeignKey(
        'receipts.SummaryReport', on_delete=models.CASCADE)
