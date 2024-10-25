from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Warehouse(models.Model):
    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склади"

    name = models.CharField(max_length=100, verbose_name="ім'я", unique=True)
    order = models.IntegerField(default=10, verbose_name="порядок")

    def __str__(self):
        return self.name


@receiver(post_save, sender=Warehouse)
def new_warehouse_created(sender, instance, created, **kwargs):
    if created:
        warehouse_dep = Department(name=instance.name, warehouse=instance)
        warehouse_dep.save()


class Department(models.Model):
    class Meta:
        verbose_name = "Підрозділ"
        verbose_name_plural = "Підрозділи"

    name = models.CharField(max_length=100, verbose_name="ім'я", unique=True)
    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name="склад",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="departments",
    )

    def __str__(self):
        return self.name
