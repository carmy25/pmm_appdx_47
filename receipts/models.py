from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseReceiptRequest(models.Model):
    number = models.CharField(verbose_name='номер', max_length=50)
    book_number = models.CharField(verbose_name='номер книги', max_length=50)
    book_series = models.CharField(verbose_name='серія книги', max_length=50)
    document_date = models.DateField(
        verbose_name='дата документу', null=True, blank=True)
    operation_date = models.DateField(verbose_name='дата операції')
    sender = models.CharField(verbose_name='відправник', max_length=50)
    destination = models.CharField(verbose_name='отримувач', max_length=50,
                                   default='А4548')
    scan = models.FileField(null=True, blank=True, verbose_name='Скан')
    fals = GenericRelation(
        'fals.FAL', object_id_field='object_id', related_query_name='document')

    @property
    def book(self):
        return f'{self.book_number}{self.book_series.upper()}'

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self._meta.verbose_name}: {self.number}/{self.book_number}{self.book_series}'

    def get_absolute_url(self):
        return reverse(f"{type(self).__name__}_detail", kwargs={"pk": self.pk})


class ReceiptRequest(BaseReceiptRequest):
    '''Definition for ReceiptRequest model.'''
    class Meta:
        verbose_name = 'чекова вимога'
        verbose_name_plural = 'чекові вимоги'
        unique_together = ('number', 'book_number', 'book_series')


class ReceiptRequestCoupon(BaseReceiptRequest):
    '''Definition for ReceiptRequestCoupon model.'''
    class Meta:
        verbose_name = 'талон чекової вимоги'
        verbose_name_plural = 'талони чекових вимог'
        unique_together = ('number', 'book_number', 'book_series')


class Certificate(models.Model):
    class Meta:
        verbose_name = 'Атестат'
        verbose_name_plural = 'Атестати'

    number = models.CharField(verbose_name='номер', max_length=50)
    sender = models.CharField(verbose_name='відправник', max_length=50)
    destination = models.CharField(verbose_name='отримувач', max_length=50,
                                   default='А4548')
    operation_date = models.DateField(verbose_name='дата операції')
    fals = GenericRelation(
        'fals.FAL', object_id_field='object_id', related_query_name='document')

    @property
    def book(self):
        return ''


class SummaryReport(models.Model):
    class Meta:
        verbose_name = 'Зведена відомість'
        verbose_name_plural = 'Зведені відомості'

    number = models.CharField(verbose_name='номер', max_length=50)
    operation_date = models.DateField(verbose_name='дата операції')
