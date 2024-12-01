from django.db import migrations


def add_measurement_scales(apps, schema_editor):
    MeasurementScale = apps.get_model('recipe_catalog', 'MeasurementScale')
    scales = [
        ('g', 'Граммы'),
        ('pcs', 'Штуки'),
        ('tbsp', 'Столовые ложки'),
        ('tsp', 'Чайные ложки'),
        ('ml', 'Миллилитры'),
    ]
    for key, label in scales:
        MeasurementScale.objects.create(key=key, label=label)


class Migration(migrations.Migration):
    dependencies = [
        ('recipe_catalog', '0015_measurementscale_and_more'),
    ]

    operations = [
        migrations.RunPython(add_measurement_scales),
    ]
