# Generated by Django 4.2.16 on 2024-11-26 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0010_ingredient_conversion_to_grams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='conversion_to_grams',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='unit',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='milliliters',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Количество миллилитров'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='pieces',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Количество штук'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='tablespoons',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Количество столовых ложек'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='teaspoons',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Количество чайных ложек'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='weight_in_grams',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Вес в граммах'),
        ),
    ]
