from django.db import models


class BaseDocument(models.Model):
    number = models.CharField(verbose_name="номер", max_length=50, unique=False)
    document_date = models.DateField(
        verbose_name="дата документу", null=True, blank=True
    )
    record_date = models.DateField(
        verbose_name="дата запису", null=True, blank=True
    )
    scan = models.FileField(null=True, blank=True, verbose_name="Скан")

    class Meta:
        abstract = True

    def verbose_scan_present(self):
        return "Так" if self.scan.name else "Ні"

    verbose_scan_present.short_description = "Скан присутній"

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.number}"
