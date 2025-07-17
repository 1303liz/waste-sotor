from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('waste_logs', '0004_update_category_details'),
    ]

    operations = [
        # Create WasteSubcategory model
        migrations.CreateModel(
            name='WasteSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('recycling_instructions', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='waste_logs.wastecategory')),
            ],
            options={
                'verbose_name_plural': 'Waste Subcategories',
            },
        ),
        
        # Add subcategory field to existing models
        migrations.AddField(
            model_name='wasteentry',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='waste_logs.wastesubcategory'),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='waste_logs.wastesubcategory'),
        ),
        
        # Update WasteLog fields
        migrations.AddField(
            model_name='wastelog',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='is_recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='recurrence_pattern',
            field=models.CharField(blank=True, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('custom', 'Custom')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='measurement_method',
            field=models.CharField(choices=[('estimated', 'Estimated'), ('weighed', 'Weighed'), ('counted', 'Counted'), ('calculated', 'Calculated')], default='estimated', max_length=50),
        ),
        
        # Update model fields for BaseWasteLog properties
        migrations.AlterField(
            model_name='wasteentry',
            name='date_logged',
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.AlterField(
            model_name='wastelog',
            name='date_logged',
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.AlterField(
            model_name='wasteentry',
            name='quantity_kg',
            field=models.FloatField(validators=[MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='wastelog',
            name='quantity_kg',
            field=models.FloatField(validators=[MinValueValidator(0.0)]),
        ),
        
        # Add the missing fields from BaseWasteLog
        migrations.AddField(
            model_name='wasteentry',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wasteentry',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='wastelog',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wastelog',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        
        # Add notes field to WasteEntry
        migrations.AddField(
            model_name='wasteentry',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        
        # Create WasteAttachment model
        migrations.CreateModel(
            name='WasteAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='waste_logs/attachments/')),
                ('file_type', models.CharField(choices=[('image', 'Image'), ('document', 'Document'), ('audio', 'Audio'), ('video', 'Video'), ('other', 'Other')], max_length=30)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('waste_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='waste_logs.wastelog')),
            ],
        ),
        
        # Create WasteGoal model
        migrations.CreateModel(
            name='WasteGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('target_quantity', models.FloatField(validators=[MinValueValidator(0.0)])),
                ('current_quantity', models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])),
                ('unit', models.CharField(default='kg', max_length=20)),
                ('start_date', models.DateField(default=timezone.now)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waste_goals', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='waste_logs.wastecategory')),
            ],
        ),
    ]
