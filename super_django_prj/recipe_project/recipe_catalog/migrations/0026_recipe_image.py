# Generated by Django 4.2.16 on 2024-12-02 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0025_measurementscale_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/', verbose_name='Изображение'),
        ),
    ]