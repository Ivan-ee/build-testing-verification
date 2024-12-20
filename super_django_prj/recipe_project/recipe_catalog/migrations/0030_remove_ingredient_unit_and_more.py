# Generated by Django 4.2.16 on 2024-12-02 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0029_remove_recipeingredient_unit_ingredient_unit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='weight_by_pcs',
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipe_catalog.measurementscale', verbose_name='Единица измерения'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='weight_by_pcs',
            field=models.IntegerField(blank=True, default=0, help_text='Если ед. изм. штуки, то указать вес на 1 штуку в граммах', null=True, verbose_name='Вес шт/гр (опционально)'),
        ),
    ]