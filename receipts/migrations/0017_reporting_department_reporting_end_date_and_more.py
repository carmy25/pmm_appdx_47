# Generated by Django 5.1 on 2024-09-10 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0003_rename_departments_departmententity_department"),
        ("receipts", "0016_alter_reporting_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="reporting",
            name="department",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="departments.department",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reporting",
            name="end_date",
            field=models.DateField(default="2023-12-12", verbose_name="Кінцева дата"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reporting",
            name="start_date",
            field=models.DateField(default="2023-11-11", verbose_name="Початкова дата"),
            preserve_default=False,
        ),
    ]
