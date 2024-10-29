from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import gettext_lazy as _


class Category(models.TextChoices):
    OIL = "OIL", _("мастило")
    DIESEL = "DIESEL", _("дизель")
    PETROL = "PETROL", _("бензин")
    POISON = "POISON", _("отрута")
    KEROSENE = "KEROSENE", _("керосин")


class FALType(models.Model):
    name = models.CharField(max_length=100, verbose_name="ім'я")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OIL,
        verbose_name="категорія",
    )
    density = models.FloatField(default=0)

    class Meta:
        verbose_name = "Тип ПММ"
        verbose_name_plural = "Типи ПММ"

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name.split('::')[0].strip()


class FAL(models.Model):
    fal_type = models.ForeignKey(
        FALType, verbose_name="тип", on_delete=models.CASCADE, related_name="fals"
    )
    amount = models.FloatField(verbose_name="кількість")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    document_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("Пально-мастильний матеріал")
        verbose_name_plural = _("Пально-мастильнi матеріали")

    def __str__(self):
        return f"{self.fal_type.name}: {self.amount}"
