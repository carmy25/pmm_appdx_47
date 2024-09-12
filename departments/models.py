from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Department(models.Model):
    class Meta:
        verbose_name = 'Підрозділ'
        verbose_name_plural = 'Підрозділи'

    name = models.CharField(max_length=100, verbose_name="ім'я", unique=True)

    def __str__(self):
        return self.name
