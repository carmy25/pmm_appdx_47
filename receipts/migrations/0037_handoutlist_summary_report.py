# Generated by Django 5.1 on 2024-10-22 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("receipts", "0036_alter_invoice_summary_report"),
        ("summary_reports", "0002_handoutlistsummaryreport"),
    ]

    operations = [
        migrations.AddField(
            model_name="handoutlist",
            name="summary_report",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="handout_lists",
                to="summary_reports.handoutlistsummaryreport",
            ),
        ),
    ]
