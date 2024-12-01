from django.db import migrations


def add_measurement_scales(apps, schema_editor):
    MeasurementScale = apps.get_model('recipe_catalog', 'MeasurementScale')
    scales = [
        ('g', 'Граммы', 'Гр'),
        ('pcs', 'Штуки', 'Шт'),
        ('tbsp', 'Столовые ложки', 'Ст.л.'),
        ('tsp', 'Чайные ложки', 'Ч.л.'),
        ('ml', 'Миллилитры', 'Мл'),
    ]

    for key, label, abbreviation in scales:
        MeasurementScale.objects.filter(key=key).update(abbreviation=abbreviation)


class Migration(migrations.Migration):
    dependencies = [
        ('recipe_catalog', '0024_measurementscale_abbreviation'),
    ]

    operations = [
        migrations.RunPython(add_measurement_scales),
    ]
