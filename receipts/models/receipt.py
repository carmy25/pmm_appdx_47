from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from .base import BaseDocument


class BaseReceiptRequest(BaseDocument):
    book_number = models.CharField(verbose_name="номер книги", max_length=50)
    book_series = models.CharField(verbose_name="серія книги", max_length=50)
    operation_date = models.DateField(verbose_name="дата операції")
    sender = models.CharField(verbose_name="відправник", max_length=50)
    destination = models.CharField(
        verbose_name="отримувач", max_length=50, default="А4548"
    )
    fals = GenericRelation(
        "fals.FAL", object_id_field="object_id", related_query_name="document"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.number}/{self.book_number}{self.book_series}"


class ReceiptRequest(BaseReceiptRequest):
    """Definition for ReceiptRequest model."""

    class Meta:
        verbose_name = "чекова вимога"
        verbose_name_plural = "чекові вимоги"
        unique_together = ("number", "book_number", "book_series")


class ReceiptRequestCoupon(BaseReceiptRequest):
    """Definition for ReceiptRequestCoupon model."""

    class Meta:
        verbose_name = "талон чекової вимоги"
        verbose_name_plural = "талони чекових вимог"
        unique_together = ("number", "book_number", "book_series")
