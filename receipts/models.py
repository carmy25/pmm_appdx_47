from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseReceiptRequest(models.Model):
    number = models.CharField(verbose_name='номер', max_length=50)
    book_number = models.CharField(verbose_name='номер книги', max_length=50)
    book_series = models.CharField(verbose_name='серія книги', max_length=50)
    operation_date = models.DateField(verbose_name='дата операції')
    fals = GenericRelation(
        'fals.FAL', object_id_field='object_id', related_query_name='document')

    class Meta:
        abstract = True


class ReceiptRequest(BaseReceiptRequest):
    '''Definition for ReceiptRequest model.'''

    def __str__(self):
        return f'чекова вимога: {self.number} {self.book_number}{self.book_series}'

    def get_absolute_url(self):
        return reverse("ReceiptRequest_detail", kwargs={"pk": self.pk})


class ReceiptRequestCoupon(BaseReceiptRequest):
    '''Definition for ReceiptRequest model.'''

    def __str__(self):
        return f'талон чекової вимоги: {self.number} {self.book_number}{self.book_series}'

    def get_absolute_url(self):
        return reverse("ReceiptRequestCoupon_detail", kwargs={"pk": self.pk})
