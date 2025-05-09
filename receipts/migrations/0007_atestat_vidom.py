# Generated by Django 5.1 on 2024-08-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("receipts", "0006_alter_receiptrequest_unique_together_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Atestat",
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
                ("sender", models.CharField(max_length=50, verbose_name="відправник")),
                (
                    "destination",
                    models.CharField(
                        default="А4548", max_length=50, verbose_name="отримувач"
                    ),
                ),
                ("operation_date", models.DateField(verbose_name="дата операції")),
            ],
            options={
                "verbose_name": "Атестат",
                "verbose_name_plural": "Атестати",
            },
        ),
        migrations.CreateModel(
            name="Vidom",
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
                    "destination",
                    models.CharField(
                        default="А4548", max_length=50, verbose_name="отримувач"
                    ),
                ),
                ("operation_date", models.DateField(verbose_name="дата операції")),
            ],
            options={
                "verbose_name": "Зведена відомість",
                "verbose_name_plural": "Зведені відомості",
            },
        ),
    ]
