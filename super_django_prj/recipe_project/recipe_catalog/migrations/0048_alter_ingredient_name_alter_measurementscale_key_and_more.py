# Generated by Django 4.2.16 on 2024-12-06 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0047_alter_ingredient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.TextField(default='Ингредиент', max_length=255, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='measurementscale',
            name='key',
            field=models.TextField(max_length=10, unique=True, verbose_name='Сокращение'),
        ),
        migrations.AlterField(
            model_name='measurementscale',
            name='label',
            field=models.TextField(max_length=50, unique=True, verbose_name='Единица измерения'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.TextField(max_length=300, verbose_name='Название блюда'),
        ),
    ]
