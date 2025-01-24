from django.db import models

# Create your models here.


class GarbageObject(models.Model):
    class Meta:
        verbose_name = "Гнидник"
        verbose_name_plural = "Гнидники"
    name = models.CharField(max_length=255, verbose_name="Назва")
    upload_date = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(verbose_name="Файл", null=True, blank=True)
    notes = models.TextField(verbose_name="Примітки", null=True, blank=True)

    def __str__(self):
        return self.name
