# Generated by Django 5.1 on 2024-08-31 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("receipts", "0011_remove_summaryreport_departments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="summaryreport",
            name="destination",
        ),
        migrations.RemoveField(
            model_name="summaryreport",
            name="sender",
        ),
    ]
