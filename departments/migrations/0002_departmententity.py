# Generated by Django 5.1 on 2024-08-31 09:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0001_initial"),
        ("receipts", "0012_remove_summaryreport_destination_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DepartmentEntity",
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
                (
                    "departments",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="departments.department",
                        verbose_name="ім'я",
                    ),
                ),
                (
                    "summary_report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="receipts.summaryreport",
                    ),
                ),
            ],
            options={
                "verbose_name": "Підрозділ",
                "verbose_name_plural": "Підрозділи",
            },
        ),
    ]
