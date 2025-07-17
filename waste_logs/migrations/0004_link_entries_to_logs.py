from django.db import migrations, models
import django.db.models.deletion

def link_entries_to_logs(apps, schema_editor):
    """
    Link existing WasteEntry objects to a default WasteLog
    """
    WasteEntry = apps.get_model('waste_logs', 'WasteEntry')
    WasteLog = apps.get_model('waste_logs', 'WasteLog')
    
    # Skip if no entries exist
    if not WasteEntry.objects.filter(waste_log__isnull=True).exists():
        return
        
    # Get or create default log
    default_log = WasteLog.objects.first()
    if not default_log:
        # We shouldn't reach here, but just in case
        default_log = WasteLog.objects.create(
            user_id=1,
            category_id=1,
            quantity_kg=0,
            title='Legacy Entries'
        )
    
    # Update all entries without a log
    WasteEntry.objects.filter(waste_log__isnull=True).update(waste_log=default_log)

class Migration(migrations.Migration):

    dependencies = [
        ('waste_logs', '0003_add_wastegoal_model'),
    ]

    operations = [
        # Run the data migration to link entries to logs
        migrations.RunPython(
            link_entries_to_logs,
            reverse_code=migrations.RunPython.noop
        ),
        # Make the waste_log field required (non-nullable)
        migrations.AlterField(
            model_name='wasteentry',
            name='waste_log',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='waste_logs.wastelog'),
        ),
    ]
