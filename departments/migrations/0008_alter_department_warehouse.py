# Generated by Django 5.1 on 2024-10-03 06:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0007_warehouse_department_warehouse"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="warehouse",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="departments",
                to="departments.warehouse",
                verbose_name="склад",
            ),
        ),
    ]
