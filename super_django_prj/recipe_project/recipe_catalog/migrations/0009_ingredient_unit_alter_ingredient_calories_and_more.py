# Generated by Django 4.2.16 on 2024-11-26 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0008_alter_recipe_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(choices=[('g', 'Граммы'), ('pcs', 'Штуки'), ('tbsp', 'Столовые ложки'), ('tsp', 'Чайные ложки'), ('ml', 'Миллилитры')], default='g', max_length=10, verbose_name='Единица измерения'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='calories',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Калорийность на 100 ед/изм', max_digits=6, verbose_name='Калорийность'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]
