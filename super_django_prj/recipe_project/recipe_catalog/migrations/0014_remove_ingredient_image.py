# Generated by Django 4.2.16 on 2024-12-01 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0013_alter_ingredient_calories_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='image',
        ),
    ]