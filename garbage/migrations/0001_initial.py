# Generated by Django 5.1 on 2025-01-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GarbageObject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Назва")),
                ("upload_date", models.DateTimeField(auto_now_add=True)),
                (
                    "attachment",
                    models.FileField(
                        blank=True, null=True, upload_to="", verbose_name="Файл"
                    ),
                ),
                (
                    "notes",
                    models.TextField(blank=True, null=True, verbose_name="Примітки"),
                ),
            ],
            options={
                "verbose_name": "Гнидник",
                "verbose_name_plural": "Гнидники",
            },
        ),
    ]
