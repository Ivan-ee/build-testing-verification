# Generated by Django 4.2.16 on 2024-11-26 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0012_remove_ingredient_milliliters_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='calories',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Калорийность на 100 ед. изм.', max_digits=6, verbose_name='Калорийность'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='conversion_to_grams',
            field=models.IntegerField(blank=True, default=0, help_text='Если ед. изм. штуки, то указать вес на 1 штуку в граммах', null=True, verbose_name='Вес шт/гр (опционально)'),
        ),
    ]
