# Generated by Django 4.2.16 on 2024-12-01 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0016_measurement_scales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='calories',
            field=models.IntegerField(default=0, help_text='Калорийность на 100 ед. изм.', verbose_name='Калорийность'),
        ),
    ]