# Generated by Django 5.1 on 2024-11-02 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("receipts", "0043_alter_inspectioncertificate_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="reporting",
            name="waybills_count",
            field=models.FloatField(
                blank=True, null=True, verbose_name="кількість шляхових"
            ),
        ),
    ]
