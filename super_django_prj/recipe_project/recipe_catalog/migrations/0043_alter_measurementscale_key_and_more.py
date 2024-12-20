# Generated by Django 4.2.16 on 2024-12-06 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0042_alter_ingredient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurementscale',
            name='key',
            field=models.CharField(max_length=10, unique=True, verbose_name='Сокращение'),
        ),
        migrations.AlterField(
            model_name='measurementscale',
            name='label',
            field=models.CharField(max_length=50, unique=True, verbose_name='Единица измерения'),
        ),
    ]
