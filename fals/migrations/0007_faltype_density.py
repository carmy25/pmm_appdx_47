# Generated by Django 5.1 on 2024-10-10 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fals', '0006_alter_fal_fal_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='faltype',
            name='density',
            field=models.FloatField(default=0),
        ),
    ]
