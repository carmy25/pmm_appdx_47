# Generated by Django 5.1 on 2024-11-03 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fals", "0009_alter_faltype_category"),
        ("receipts", "0044_reporting_waybills_count"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvoiceForRRC",
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
            ],
            options={
                "verbose_name": "Накладна для талон. чек. вимог.",
                "verbose_name_plural": "Накладні для талон. чек. вимог.",
            },
        ),
        migrations.AlterField(
            model_name="reporting",
            name="state",
            field=models.CharField(
                choices=[
                    ("NEW", "нове"),
                    ("WITH_ERROR", "містить помилку"),
                    ("CHECKED", "перевірено"),
                    ("GO_AWAY", "здано в ФЕС"),
                    ("COMPLETED", "проведено"),
                ],
                default="NEW",
                max_length=20,
                verbose_name="стан",
            ),
        ),
        migrations.CreateModel(
            name="InvoiceForRRCEntry",
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
                ("amount", models.FloatField(verbose_name="видано")),
                (
                    "fal_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fal_rrc_entries",
                        to="fals.faltype",
                        verbose_name="тип",
                    ),
                ),
                (
                    "rrc",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fals",
                        to="receipts.receiptrequestcoupon",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пально-мастильний матеріал",
                "verbose_name_plural": "Пально-мастильнi матеріали",
            },
        ),
    ]
