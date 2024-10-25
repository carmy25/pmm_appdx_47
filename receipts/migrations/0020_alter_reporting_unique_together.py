# Generated by Django 5.1 on 2024-09-11 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0004_alter_department_name"),
        ("receipts", "0019_reporting_note_reporting_state_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="reporting",
            unique_together={("department", "start_date", "end_date")},
        ),
    ]
