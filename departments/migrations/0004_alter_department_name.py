# Generated by Django 5.1 on 2024-09-11 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0003_rename_departments_departmententity_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name="ім'я"),
        ),
    ]
