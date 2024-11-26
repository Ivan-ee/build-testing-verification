# Generated by Django 4.2.16 on 2024-11-04 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0005_ingredient_calories_recipe_servings_recipe_weight_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='servings',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='weight',
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='weight',
            field=models.DecimalField(decimal_places=1, default=0.0, help_text='Вес в граммах', max_digits=6),
        ),
    ]