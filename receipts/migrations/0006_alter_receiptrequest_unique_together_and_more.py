# Generated by Django 5.1 on 2024-08-23 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("receipts", "0005_alter_receiptrequest_document_date_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="receiptrequest",
            unique_together={("number", "book_number", "book_series")},
        ),
        migrations.AlterUniqueTogether(
            name="receiptrequestcoupon",
            unique_together={("number", "book_number", "book_series")},
        ),
    ]
