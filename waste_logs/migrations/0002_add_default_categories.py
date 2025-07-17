from django.db import migrations

def create_default_categories(apps, schema_editor):
    # Make sure to only use the models provided by the migration framework
    WasteCategory = apps.get_model('waste_logs', 'WasteCategory')
    
    # Create main categories with only the name field (the only field available in the initial migration)
    categories = [
        'Plastic',
        'Paper',
        'Glass',
        'Metal',
        'Organic',
        'Electronic',
        'Hazardous',
        'Textile',
        'Non-recyclable'
    ]
    
    # Create the categories
    for name in categories:
        WasteCategory.objects.create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('waste_logs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]
