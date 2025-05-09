# Generated by Django 5.1 on 2024-10-04 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("receipts", "0028_rename_receiver_invoice_destination"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvoiceSummaryReport",
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
                ("start_date", models.DateField(verbose_name="початкова дата")),
                ("end_date", models.DateField(verbose_name="кінцева дата")),
            ],
            options={
                "verbose_name": "Зведена відомість по накладних",
                "verbose_name_plural": "Зведені відомості по накладних",
            },
        ),
        migrations.AddField(
            model_name="invoice",
            name="summary_report",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="invoices",
                to="receipts.invoicesummaryreport",
            ),
        ),
    ]
