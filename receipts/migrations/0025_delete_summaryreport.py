# Generated by Django 5.1 on 2024-09-12 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0005_remove_departmententity_summary_report"),
        ("receipts", "0024_alter_reporting_summary_report"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SummaryReport",
        ),
    ]
