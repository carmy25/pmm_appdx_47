# Generated by Django 5.1 on 2024-12-11 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0011_department_chief_name_department_chief_position"),
        ("receipts", "0057_alter_invoiceforrrcentry_fal_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="handoutlist",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="receiver_handouts",
                to="departments.department",
                verbose_name="отримувач",
            ),
        ),
        migrations.AlterField(
            model_name="handoutlist",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sender_handouts",
                to="departments.department",
                verbose_name="відправник",
            ),
        ),
    ]
