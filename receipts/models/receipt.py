from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from fals.models import FALType
from receipts.models.certificate import Certificate

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


class InvoiceForRRC(BaseDocument):
    class Meta:
        verbose_name = 'Накладна для талон. чек. вимог.'
        verbose_name_plural = 'Накладні для талон. чек. вимог.'
    rrc = models.ForeignKey(
        ReceiptRequestCoupon, on_delete=models.CASCADE, related_name="invoices",
        blank=True, null=True)

    certificate = models.ForeignKey(
        Certificate, on_delete=models.CASCADE, related_name="invoices",
        blank=True, null=True)


class InvoiceForRRCEntry(models.Model):
    class Meta:
        verbose_name = "Пально-мастильний матеріал"
        verbose_name_plural = "Пально-мастильнi матеріали"
    fal_type = models.ForeignKey(
        FALType,
        verbose_name="тип",
        on_delete=models.CASCADE,
        related_name="fal_rrc_entries",
    )
    invoice_for_rrc = models.ForeignKey(
        InvoiceForRRC, on_delete=models.CASCADE, related_name="fals")
    amount = models.FloatField(verbose_name="видано")
    price = models.FloatField(verbose_name="сума (в грн)")
