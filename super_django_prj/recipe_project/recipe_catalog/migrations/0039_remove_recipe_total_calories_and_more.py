# Generated by Django 4.2.16 on 2024-12-03 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0038_recipe_total_calories_recipe_total_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='total_calories',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='total_weight',
        ),
    ]