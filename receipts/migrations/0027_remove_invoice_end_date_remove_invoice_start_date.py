# Generated by Django 5.1 on 2024-09-14 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("receipts", "0026_invoice"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invoice",
            name="end_date",
        ),
        migrations.RemoveField(
            model_name="invoice",
            name="start_date",
        ),
    ]
