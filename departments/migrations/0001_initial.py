# Generated by Django 5.1 on 2024-08-31 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name="ім'я")),
            ],
            options={
                'verbose_name': 'Підрозділ',
                'verbose_name_plural': 'Підрозділи',
            },
        ),
    ]
