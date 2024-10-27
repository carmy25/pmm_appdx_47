from django.db import models
from django.utils.translation import gettext_lazy as _
from departments.models import Department
from fals.models import FALType
from summary_reports.models import ReportingSummaryReport

from .base import BaseDocument


class Reporting(BaseDocument):
    class Meta:
        verbose_name = "Донесення"
        verbose_name_plural = "Донесення"
        unique_together = ("department", "start_date", "end_date")

    number = models.CharField(
        verbose_name="номер", null=True, blank=True, max_length=50
    )

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, verbose_name="підрозділ"
    )
    summary_report = models.ForeignKey(
        ReportingSummaryReport,
        null=True,
        related_name="reportings",
        on_delete=models.SET_NULL,
    )

    start_date = models.DateField(verbose_name="початкова дата")
    end_date = models.DateField(verbose_name="кінцева дата")

    class Category(models.TextChoices):
        NEW = "NEW", _("нове")
        WITH_ERROR = "WITH_ERROR", _("містить помилку")
        CHECKED = "CHECKED", _("перевірено")
        GO_AWAY = "GO_AWAY", _("здано")
        COMPLETED = "COMPLETED", _("проведено")

    state = models.CharField(
        default=Category.NEW,
        max_length=20,
        verbose_name="стан",
        choices=Category.choices,
    )
    note = models.CharField(
        max_length=500, verbose_name="нотатка", blank=True, null=True
    )

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.number or 'без номеру'}({self.department.name})"


class FALReportEntry(models.Model):
    fal_type = models.ForeignKey(
        FALType,
        verbose_name="тип",
        on_delete=models.CASCADE,
        related_name="fal_report_entries",
    )

    report = models.ForeignKey(Reporting, on_delete=models.CASCADE, related_name="fals")

    density = models.FloatField(verbose_name="густина", null=True, blank=True)

    remains = models.FloatField(verbose_name="залишок")
    income = models.FloatField(verbose_name="надійшло")
    outcome = models.FloatField(verbose_name="вибуло")

    class Meta:
        verbose_name = _("Пально-мастильний матеріал")
        verbose_name_plural = _("Пально-мастильнi матеріали")

    def get_density(self):
        return self.density or self.fal_type.density
