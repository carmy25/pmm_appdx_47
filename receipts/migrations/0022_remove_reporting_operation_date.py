# Generated by Django 5.1 on 2024-09-11 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0021_alter_reporting_operation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporting',
            name='operation_date',
        ),
    ]
