# Generated by Django 4.2.16 on 2024-12-01 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0020_alter_recipeingredient_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeingredient',
            name='weight',
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='count',
            field=models.IntegerField(default=0, help_text='Количество'),
        ),
    ]
