from django.db import models


class Warehouse(models.Model):
    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склади'

    name = models.CharField(max_length=100, verbose_name="ім'я", unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    class Meta:
        verbose_name = 'Підрозділ'
        verbose_name_plural = 'Підрозділи'

    name = models.CharField(max_length=100, verbose_name="ім'я", unique=True)
    warehouse = models.ForeignKey(Warehouse, verbose_name='склад',
                                  null=True,
                                  on_delete=models.CASCADE,
                                  related_name='departments')

    def __str__(self):
        return self.name
