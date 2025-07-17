from django.db import migrations

def update_category_details(apps, schema_editor):
    # Get the WasteCategory model from apps
    WasteCategory = apps.get_model('waste_logs', 'WasteCategory')
    
    # Dictionary of category details
    category_details = {
        'Plastic': {
            'description': 'Various plastic waste items',
            'icon': 'fa-wine-bottle',
            'color': '#E57373',
            'is_recyclable': True,
        },
        'Paper': {
            'description': 'Paper and cardboard items',
            'icon': 'fa-newspaper',
            'color': '#81C784',
            'is_recyclable': True,
        },
        'Glass': {
            'description': 'Glass containers and items',
            'icon': 'fa-wine-glass',
            'color': '#64B5F6',
            'is_recyclable': True,
        },
        'Metal': {
            'description': 'Metal containers and items',
            'icon': 'fa-utensils',
            'color': '#90A4AE',
            'is_recyclable': True,
        },
        'Organic': {
            'description': 'Food and garden waste',
            'icon': 'fa-apple-alt',
            'color': '#AED581',
            'is_compostable': True,
        },
        'Electronic': {
            'description': 'Electronic devices and components',
            'icon': 'fa-laptop',
            'color': '#FFD54F',
            'is_hazardous': True,
        },
        'Hazardous': {
            'description': 'Toxic or dangerous materials',
            'icon': 'fa-skull',
            'color': '#FF8A65',
            'is_hazardous': True,
        },
        'Textile': {
            'description': 'Clothing and fabric items',
            'icon': 'fa-tshirt',
            'color': '#BA68C8',
            'is_recyclable': True,
        },
        'Non-recyclable': {
            'description': 'Items that typically go to landfill',
            'icon': 'fa-trash-alt',
            'color': '#78909C',
        },
    }
    
    # Update each category
    for name, details in category_details.items():
        category = WasteCategory.objects.filter(name=name).first()
        if category:
            for field, value in details.items():
                setattr(category, field, value)
            category.save()


class Migration(migrations.Migration):

    dependencies = [
        ('waste_logs', '0003_add_category_fields'),
    ]

    operations = [
        migrations.RunPython(update_category_details),
    ]
