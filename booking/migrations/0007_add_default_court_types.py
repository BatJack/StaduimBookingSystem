from django.db import migrations


def create_default_court_types(apps, schema_editor):
    CourtType = apps.get_model('booking', 'CourtType')
    default_types = [
        '篮球场',
        '网球场',
        '羽毛球场',
        '匹克球场',
        '台球场',
    ]
    for name in default_types:
        CourtType.objects.get_or_create(
            name=name,
            defaults={'is_default': True}
        )


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_add_court_type'),
    ]

    operations = [
        migrations.RunPython(create_default_court_types),
    ]
