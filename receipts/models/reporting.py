from django.db import models
from django.utils.translation import gettext_lazy as _
from departments.models import Department
from fals.models import Category, FALType
from summary_reports.models import ReportingSummaryReport

from .base import BaseDocument


class Reporting(BaseDocument):
    class Meta:
        verbose_name = "Донесення"
        verbose_name_plural = "Донесення"
        unique_together = ("department", "start_date", "end_date")

    number = models.CharField(
        verbose_name="номер", null=True, blank=True, max_length=50, unique=False
    )

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, verbose_name="підрозділ",
        related_name='reportings'
    )
    summary_report = models.ForeignKey(
        ReportingSummaryReport,
        null=True,
        related_name="documents",
        on_delete=models.SET_NULL,
    )

    start_date = models.DateField(verbose_name="початкова дата")
    end_date = models.DateField(verbose_name="кінцева дата")

    class Category(models.TextChoices):
        NEW = "NEW", _("нове")
        WITH_ERROR = "WITH_ERROR", _("містить помилку")
        CHECKED = "CHECKED", _("перевірено")
        GO_AWAY = "GO_AWAY", _("здано в ФЕС")
        COMPLETED = "COMPLETED", _("проведено")

    state = models.CharField(
        default=Category.NEW,
        max_length=20,
        verbose_name="стан",
        choices=Category.choices,
    )
    waybills_numbers = models.TextField(verbose_name="номера шляхових", null=True, blank=True)
    handout_numbers = models.TextField(
        verbose_name="номера роздавальних відомостей", null=True, blank=True)
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

    remains = models.FloatField(verbose_name="залишок (л)")
    income = models.FloatField(verbose_name="надійшло (л)")
    outcome_burned_ltr = models.FloatField(
        verbose_name="спалено (л)",
    )
    outcome_burned = models.FloatField(
        verbose_name="спалено (кг)",
    )
    outcome = models.FloatField(verbose_name="вибуло")

    class Meta:
        verbose_name = _("Пально-мастильний матеріал")
        verbose_name_plural = _("Пально-мастильнi матеріали")

    def get_density(self):
        return self.density or self.fal_type.density

    def get_outcome_kgs(self):
        return self.get_kgs(self.outcome)

    def get_burned_kgs(self):
        return self.outcome_burned

    def get_income_kgs(self):
        return self.get_kgs(self.income)

    def get_kgs(self, val):
        kgs = self.get_density() * val
        if self.fal_type.category in [Category.PETROL,
                                      Category.DIESEL,
                                      Category.KEROSENE]:
            return round(kgs)
        elif self.fal_type.category == Category.OIL:
            return round(kgs, 1)
        return round(kgs, 2)

    def get_remains_after_kgs(self):
        return self.get_kgs(self.income) + self.get_kgs(self.remains) - self.get_outcome_kgs()
