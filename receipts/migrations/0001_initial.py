# Generated by Django 5.1 on 2024-08-23 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, verbose_name='номер')),
                ('book_number', models.CharField(max_length=50, verbose_name='номер книги')),
                ('book_series', models.CharField(max_length=50, verbose_name='серія книги')),
                ('operation_date', models.DateField(verbose_name='дата операції')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReceiptRequestCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, verbose_name='номер')),
                ('book_number', models.CharField(max_length=50, verbose_name='номер книги')),
                ('book_series', models.CharField(max_length=50, verbose_name='серія книги')),
                ('operation_date', models.DateField(verbose_name='дата операції')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
