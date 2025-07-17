from django.db import migrations, models
import django.db.models.deletion

def create_default_waste_log(apps, schema_editor):
    """
    Create a default WasteLog for existing WasteEntry objects if there are any
    """
    WasteEntry = apps.get_model('waste_logs', 'WasteEntry')
    WasteLog = apps.get_model('waste_logs', 'WasteLog')
    User = apps.get_model('auth.User')
    WasteCategory = apps.get_model('waste_logs', 'WasteCategory')
    
    # Check if there are any existing entries
    if not WasteEntry.objects.exists():
        return
    
    # Create a default log for the entries to link to
    user = User.objects.first()
    if not user:
        return
        
    category = WasteCategory.objects.first()
    if not category:
        return
    
    default_log = WasteLog.objects.create(
        user=user,
        category=category,
        quantity_kg=0,
        title='Legacy Entries'
    )
    
    # Link all existing entries to this log
    WasteEntry.objects.update(waste_log=default_log)

class Migration(migrations.Migration):

    dependencies = [
        ('waste_logs', '0005_add_models_and_fields'),
    ]

    operations = [
        # Add waste_log field to WasteEntry
        migrations.AddField(
            model_name='wasteentry',
            name='waste_log',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='waste_logs.wastelog'),
        ),
        # Run the data migration to link entries to the default log
        migrations.RunPython(
            create_default_waste_log,
            reverse_code=migrations.RunPython.noop
        ),
        # Make the field required (not nullable)
        migrations.AlterField(
            model_name='wasteentry',
            name='waste_log',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='waste_logs.wastelog'),
        ),
    ]
