# Generated by Django 4.2.16 on 2024-12-06 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0046_alter_ingredient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(default='Ингредиент', max_length=255, unique=True, verbose_name='Название'),
        ),
    ]
