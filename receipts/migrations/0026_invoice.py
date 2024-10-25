# Generated by Django 5.1 on 2024-09-14 09:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0006_delete_departmententity"),
        ("receipts", "0025_delete_summaryreport"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
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
                ("number", models.CharField(max_length=50, verbose_name="номер")),
                (
                    "document_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="дата документу"
                    ),
                ),
                (
                    "scan",
                    models.FileField(
                        blank=True, null=True, upload_to="", verbose_name="Скан"
                    ),
                ),
                ("operation_date", models.DateField(verbose_name="дата операції")),
                ("start_date", models.DateField(verbose_name="початкова дата")),
                ("end_date", models.DateField(verbose_name="кінцева дата")),
                (
                    "responsible_person",
                    models.CharField(
                        max_length=233, verbose_name="відповідальна особа"
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invoices_receiver",
                        to="departments.department",
                        verbose_name="отримувач",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invoices_sender",
                        to="departments.department",
                        verbose_name="відправник",
                    ),
                ),
            ],
            options={
                "verbose_name": "Накладна",
                "verbose_name_plural": "Накладні",
            },
        ),
    ]
